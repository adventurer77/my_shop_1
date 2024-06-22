from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages

# Create your views here.


def index(request):

    context = {
        "title": "Home place",
        "content": "Furniture store HOME PLACE",
    }
    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "Adout us",
        "content": "Adout us",
        "text_on_page": "HOME PLACE is the best furniture store in the world",
    }

    return render(request, "main/about.html", context)


def contact(request):
    form = ContactForm(request.POST)
    context = {
        "title": "Contact Us",
        "contact_button": "Send Message",
        "form" : form
    }
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you for your question, we will contact you as soon as possible.")
        return render(request, "main/index.html", context)
    else:

        messages.error(
            request,
            "There were errors in your form. Please correct and try again.",
        )

        return render(request, "main/contact_us.html", context)