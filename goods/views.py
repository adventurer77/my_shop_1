from django.http import Http404
from django.shortcuts import render,redirect
from django.core.paginator import Paginator

from goods.models import Products
from goods.utils import q_search

# Create your views here.


def catalog(request, category_slug=None):

    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)


    if category_slug == "all" :

        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            # raise Http404("No Products found matching the category.")
            return redirect("main:index")


    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    
    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        "title_Catalog": "Catalog",
        "goods": current_page,
        "slug_url": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request,product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        "product" : product,
        "ad_to_cart_btn" : "Add to cart",
    }

    return render(request, "goods/product.html",context=context)
