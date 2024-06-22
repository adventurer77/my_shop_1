from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from carts.models import Cart
from goods.models import Products
from carts.utils import get_user_carts

# Create your views here.


def cart_add(request):
    
    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart =  carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product
        )

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1
            )


    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )
        
    responce_date = {
        "message" : "Product add to cart",
        "cart_items_html" : cart_items_html,
    }
        
    return JsonResponse(responce_date)

    # return redirect(request.META["HTTP_REFERER"])

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity
    

    # cart = get_user_carts(request)
    user_cart = get_user_carts(request)

    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["is_order"] = True

    cart_items_html = render_to_string(
            "carts/includes/included_cart.html", context, request=request
            # "carts/includes/included_cart.html", {"carts": cart}, request=request,
            
        )
    
    responce_date = {
           "message" : "Number of products changed",
           "cart_items_html" : cart_items_html,
           "quantity": updated_quantity,
    }

    return JsonResponse(responce_date)

def cart_remove(request):

    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)

    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get('HTTP_REFERER')
    if reverse('orders:create_order') in referer:
        context["is_order"] = True

    cart_items_html = render_to_string(
            "carts/includes/included_cart.html", context, request=request
            # "carts/includes/included_cart.html", {"carts": user_cart}, request=request
            
        )
    
    a = '/'+'/'.join(request.META['HTTP_REFERER'].split('/')[3:])
    b = reverse("orders:create_order")

    if len(user_cart) == 0 and a == b:
        redirect_to_home = True
    else:
        redirect_to_home = False

    response_data = {
        "message": "Product removed from cart",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
        "redirect_to_home": redirect_to_home
    }

    return JsonResponse(response_data)


    # responce_date = {
    #        "message" : "Product removed from cart",
    #        "cart_items_html" : cart_items_html,
    #        "quantity_deleted": quantity,
    # }
        
    # return JsonResponse(responce_date)

    # cart = Cart.objects.get(id=cart_id)
    # cart.delete()
    # return redirect(request.META["HTTP_REFERER"])