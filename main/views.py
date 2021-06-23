from django.shortcuts import render, get_object_or_404
from .models import Item, Reviews
from django.contrib.auth.decorators import login_required
from .decorators import *


def home(request):
    menu = get_object_or_404(Menu, description="Display")
    restaurants = Restaurant.objects.all()
    # get all items in menu
    items = menu.items.all()
    print(restaurant)

    context = {
        'items': items,
        'restaurants': restaurants,
    }
    return render(request, 'main/home.html', context)


def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    restaurants = Restaurant.objects.all()
    # getting the first 7 reviews
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7]
    avail = int(item.quantity_available)
    loop_times = range(1, avail+1)
    '''
    if request.method == 'POST':
        quantity = request.POST.get("quantity")
        avail = avail - int(quantity)
        item.update(quantity_available=avail)
        loop_times = range(1, avail+1)
    '''
    context = {
        'item': item,
        'restaurants': restaurants,
        'reviews': reviews,
        'loop_times': loop_times,
    }
    return render(request, 'main/dishes.html', context)


def restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurants = Restaurant.objects.all()
    # get all menu available in restaurants
    items = restaurant.menu_available.all()
    name = restaurant.place.name
    print(name)
    context = {
        'items': items,
        'name': name,
        'restaurants': restaurants,
    }
    return render(request, 'main/restaurant.html', context)
