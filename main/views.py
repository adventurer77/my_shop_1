
from django.shortcuts import render

from goods.models import Categories

# Create your views here.

def index(request):

    context= {
        "title" : "Home place",
        "content" : "Furniture store HOME PLACE", 
    }
    return  render(request, "main/index.html", context)


def about(request):
    context = {
        'title': 'Adout us',
        'content': "Adout us",
        'text_on_page': "HOME PLACE is the best furniture store in the world"
    }

    return render(request, 'main/about.html', context)


