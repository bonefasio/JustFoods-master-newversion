from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from main.models import Item, OrderItems, Reviews
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.decorators import *
from django.db.models import Sum
# from main.forms import PayrollRegistrationForm, SubscriptionForm, OrderItemForm
import datetime
from datetime import timedelta


# Create your views here.
@login_required(login_url='/accounts/login/')
def menuDetail(request, slug):
    customer = request.user.customer
    item = Item.objects.filter(slug=slug).first()
    restaurants = Restaurant.objects.all()
    # getting the first 7 reviews
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7]
    avail_item = int(item.quantity_available)
    loop_times = range(1, avail_item+1)

    ordered_date = timezone.now()

    if request.method == 'POST':
        quantity = request.POST.get("quantity")
        quantity = int(quantity)  # casting quantity to int
        avail = avail_item - int(quantity)
        item.quantity_available = avail  # updating quantity values
        loop_times = range(1, avail+1)
        print(quantity)
        order_item = OrderItems.objects.create(
            item=item, customer=customer, ordered=False, quantity=quantity, ordered_date=ordered_date, subscription_order=False)
        order_item.save()

        messages.info(request, "Added to Order!!Continue Shopping!!")
        return redirect("orders:cart")

    context = {
        'item': item,
        'restaurants': restaurants,
        'reviews': reviews,
        'loop_times': loop_times,
    }
    return render(request, 'orders/dishes.html', context)


@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thankyou for reviewing this product!!")
    return redirect(f"/dishes/{item.slug}")


@login_required
def get_cart_items(request):
    customer = request.user.customer
    restaurants = Restaurant.objects.all()
    ordered_items = OrderItems.objects.filter(
        customer=customer, ordered=False, subscription_order=False)

    total = 0
    total_list = []  # list of total of each subscription order
    for orders in ordered_items:
        totals = orders.get_total
        total_list.append(totals)

    # Iterate each element in list and add them in variable total
    for ele in range(0, len(total_list)):
        total = total + total_list[ele]

    number = ordered_items.aggregate(Sum('quantity'))
    count = number.get("quantity__sum")  # sum of quantity

    context = {
        'ordered_items': ordered_items,
        'total': total,
        'count': count,
        'restaurants': restaurants,
    }
    return render(request, 'orders/cart.html', context)


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'orders/cartitems_confirm_delete.html'
    success_url = '/orders/cart'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the restaurants
        context['restaurants'] = Restaurant.objects.all()
        return context

    def test_func(self):
        cart = self.get_object()
        if self.request.user.customer == cart.customer:
            return True
        return False


@login_required
def order_delivery(request):
    customer = request.user.customer
    restaurants = Restaurant.objects.all()
    items = OrderItems.objects.filter(
        customer=customer, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered

    total = 0
    total_list = []  # list of total of each subscription order
    for orders in items:
        totals = orders.get_total
        total_list.append(totals)

    # Iterate each element in list and add them in variable total
    for ele in range(0, len(total_list)):
        total = total + total_list[ele]

    number = items.aggregate(Sum('quantity'))
    count = number.get("quantity__sum")  # sum of quantity

    offsite = Location.objects.filter(category="OffSite")  # offsite locations
    onsite = Location.objects.filter(category="OnSite")  # onsite locations
    pickup_location = Location.objects.get(
        category="Direct Pickup")  # direct pickup location

    if request.method == 'POST':  # collecting data from html forms
        payment_method = request.POST.get("payment_method")
        delivery_date = request.POST.get("delivery_date")
        delivery_time = request.POST.get("delivery_time")
        delivery_mode = request.POST.get("delivery_mode")
        location = request.POST.get("location")
        onsite_delivery_location = request.POST.get("onsite_location")
        offsite_delivery_location = request.POST.get("offsite_location")
        # combining date and time
        delivery_date_modified = datetime.datetime.strptime(
            str(delivery_date), "%Y-%m-%d").date()
        delivery_time_modified = datetime.datetime.strptime(
            str(delivery_time), "%H:%M").time()

        delivery_date_time = datetime.datetime.combine(
            delivery_date_modified, delivery_time_modified)

        print('Delivery date : ')
        print(delivery_date_time)

        if delivery_mode == 'pickup':
            items.update(payment_method=payment_method, delivery_date=delivery_date_time,
                         delivery_mode=delivery_mode, delivery_location=pickup_location)

        if delivery_mode == 'deliver' and location == 'onsite':
            location_on = Location.objects.get(
                id=onsite_delivery_location)  # get onsite location
            items.update(payment_method=payment_method, delivery_date=delivery_date,
                         delivery_mode=delivery_mode, delivery_location=location_on)
           # print('Youre opting for onsite delivery')

        if delivery_mode == 'deliver' and location == 'offsite':
            location_off = Location.objects.get(
                id=offsite_delivery_location)  # get offsite location
            items.update(payment_method=payment_method, delivery_date=delivery_date,
                         delivery_mode=delivery_mode, delivery_location=location_off)
           # print('Youre opting for offsite delivery')

        if request.POST.get("payment_method") == 'Debit/Credit Card':
            return redirect('stripepayment:index')  # redirect to stripe page

        messages.info(request, "Delivery details saved")
        # redirect to a new URL:
        return redirect('payrollpayment:payment-page')

    context = {
        'items': items,
        'total': total,
        'count': count,
        'offsite': offsite,
        'onsite': onsite,
        'restaurants': restaurants,
    }
    return render(request, 'orders/order_delivery.html', context)


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'orders/orderitems_confirm_delete.html'
    success_url = '/orders/order_delivery'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the restaurants
        context['restaurants'] = Restaurant.objects.all()
        return context

    def test_func(self):
        subscribing = self.get_object()
        if self.request.user.customer == subscribing.customer:
            return True
        return False


@login_required
def order_details(request):
    customer = request.user.customer
    restaurants = Restaurant.objects.all()
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active").order_by('-ordered_date')  # not yet been delivered
    order_items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Delivered", isPaid=True).order_by('-ordered_date')  # delivered and paid orders

    total = 0
    total_list = []  # list of total of each subscription order
    for orders in items:
        totals = orders.get_total
        total_list.append(totals)

    # Iterate each element in list and add them in variable total
    for ele in range(0, len(total_list)):
        total = total + total_list[ele]

    number = items.aggregate(Sum('quantity'))
    count = number.get("quantity__sum")  # sum of quantity
    # count = OrderItems.objects.filter()
    context = {
        'items': items,
        'order_items': order_items,  # Delivered Items
        'total': total,
        # 'past_orders_total': past_orders_total,
        'count': count,
        'restaurants': restaurants,
    }
    return render(request, 'orders/order_details.html', context)


@login_required
def delivery_details(request):
    customer = request.user.customer
    restaurants = Restaurant.objects.all()
    # items = OrderItems.objects.filter(
    # customer=customer, ordered=True, status="Active").order_by('-ordered_date')
    order_items = OrderItems.objects.filter(
        customer=customer, ordered=True, isPaid=True).order_by('-ordered_date')
    bill = order_items.aggregate(Sum('item__price'))
    number = order_items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity
    # count = OrderItems.objects.filter()
    context = {
        # 'items': items,
        'order_items': order_items,  # Delivered Items
        'total': total,
        'count': count,
        'restaurants': restaurants,
    }
    return render(request, 'orders/delivery_details.html', context)
