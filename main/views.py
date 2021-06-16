from django.shortcuts import render, get_object_or_404
#from django.urls import reverse_lazy
from .models import Item, Reviews
from django.contrib.auth.decorators import login_required
from .decorators import *


def home(request):
    menu = get_object_or_404(Menu, description="Display")
    # get all items in menu
    items = menu.items.all()
    print(items)

    context = {
        'items': items,
    }
    return render(request, 'main/home.html', context)


def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    #item = get_object_or_404(Item, slug=slug)
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
        'reviews': reviews,
        'loop_times': loop_times,
    }
    return render(request, 'main/dishes.html', context)
