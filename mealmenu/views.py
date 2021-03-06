from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from main.models import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from main.decorators import *
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


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


@login_required
def lunch(request):
    restaurants = Restaurant.objects.all()
    menu = get_object_or_404(Menu, description="Lunch")
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
    return render(request, 'mealmenu/lunch.html', context)


@login_required
def dinner(request):
    menu = get_object_or_404(Menu, description="Dinner")
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
    return render(request, 'mealmenu/dinner.html', context)


@login_required
def breakfast(request):
    menu = get_object_or_404(Menu, description="Breakfast")
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
    return render(request, 'mealmenu/breakfast.html', context)


@login_required
def custom_meal(request):
    restaurants = Restaurant.objects.all()

    if request.method == "POST":
        custom_meal_name = request.POST.get("custom_meal_name")
        patron_first_name = request.POST.get("patron_first_name")
        patron_last_name = request.POST.get("patron_last_name")
        patron_email_address = request.POST.get("patron_email_address")
        patron_phone_contact = request.POST.get("patron_phone_contact")
        meal_reqest_time = request.POST.get("meal_reqest_time")
        meal_request_date = request.POST.get("meal_request_date")
        order_quantity = request.POST.get("order_quantity")
        custom_meal_receipe = request.POST.get("custom_meal_receipe")
        custom_meal_ingredients = request.POST.get("custom_meal_ingredients")

        custom_meal = CustomMeal(custom_meal_name=custom_meal_name, patron_first_name=patron_first_name,
                                 patron_last_name=patron_last_name,
                                 patron_email_address=patron_email_address,
                                 patron_phone_contact=patron_phone_contact,
                                 meal_request_date=meal_request_date, order_quantity=order_quantity,
                                 custom_meal_receipe=custom_meal_receipe,
                                 custom_meal_ingredients=custom_meal_ingredients)
        custom_meal.save()
        messages.success(
            request, "Custom Meal Request Sent, Kindly Wait For Cafeteria Response!!")

    context = {
        'restaurants': restaurants,
    }
    return render(request, 'mealmenu/custom_meal.html', context)
