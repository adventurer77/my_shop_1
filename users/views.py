from django.contrib.auth.decorators import login_required
from django.contrib import auth ,messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Prefetch


from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from carts.models import Cart
from orders.models import Order, OrderItem

# Create your views here.

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, You're logged in to your account.")

                if session_key:
                     # delete old authorized user carts
                    forgot_carts = Cart.objects.filter(user=user)
                    if forgot_carts.exists():
                        forgot_carts.delete()
                    # add new authorized user carts from anonimous session
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                # if request.POST.get("next", None):
                if redirect_page and redirect_page != reverse("user:logout"):
                   return HttpResponseRedirect(request.POST.get("next"))

                return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserLoginForm()

    context = {
        "title": "Authorization",
        "log_in_btn": "Log in",
        "create_an_account_btn": "Create an account",
        "form": form
    }
    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            
            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)
            
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"{user.username}, You have successfully registered and logged in to your account.")
            return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserRegistrationForm()

    context = {
        "title": "Registration",
        "personal_account_btn": "Create a personal account",
        "form": form
    }
    return render(request, "users/registration.html", context)

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated.")
            return HttpResponseRedirect(reverse("user:profile"))

    else:
        form = ProfileForm(instance=request.user)


    orders = (
        Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product")
            )
        ).order_by("id")
    )

    context = {
        "title": "Profile",
        "save_btn": "Save",
        "my_orders": "My orders",
        'order_labels': {
            'item': ('Product'),
            'quantity': ('Quantity'),
            'price': ('Price'),
            'total_price': ('Total price'),
        },
        "form": form,
        "orders": orders
    }
    return render(request, "users/profile.html", context)


def users_cart(request):
    return render(request, "users/users_cart.html")

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, You've logged out of your account.")
    auth.logout(request)
    return redirect(reverse("main:index"))