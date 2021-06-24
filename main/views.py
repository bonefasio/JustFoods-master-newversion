from django.shortcuts import render, get_object_or_404
from .models import Item, Reviews
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def home(request):
    menu = get_object_or_404(Menu, description="Display")
    restaurants = Restaurant.objects.all()
    # get all items in menu
    item_list = menu.items.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(item_list, 3)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'restaurants': restaurants,
    }
    return render(request, 'main/home.html', context)


@login_required(login_url='/accounts/login/')
def restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurants = Restaurant.objects.all()
    name = restaurant.place.name
    # get all menu available in restaurants
    item_list = restaurant.menu_available.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(item_list, 3)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'name': name,
        'restaurants': restaurants,
    }
    return render(request, 'main/restaurant.html', context)
