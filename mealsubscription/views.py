from django.shortcuts import render
from django.urls import reverse_lazy
from main.models import *
# from main.models import MealSubscription
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from main.decorators import *
from django.db.models import Sum
#from main.forms import SubscriptionForm
from datetime import timedelta
import datetime
# Create your views here.


@login_required(login_url='/accounts/login/')
def subscriptionDetail(request, slug):
    customer = request.user.customer
    restaurants = Restaurant.objects.all()
    item = Item.objects.filter(slug=slug, subcription_avail=True).first()
    subscription_ordered_items = OrderItems.objects.filter(
        item=item, customer=customer, subscription_order=True)

    total = 0
    total_list = []  # list of total of each subscription order
    for orders in subscription_ordered_items:
        totals = orders.get_total
        total_list.append(totals)

    # Iterate each element in list
    # and add them in variable total
    for ele in range(0, len(total_list)):
        total = total + total_list[ele]

    number = subscription_ordered_items.aggregate(Sum('quantity'))
    count = number.get("quantity__sum")  # sum of quantity

    context = {
        'item': item,
        'subscription_ordered_items': subscription_ordered_items,
        'total': total,
        'count': count,
        'restaurants': restaurants,
    }
    return render(request, 'mealsubscription/subscription.html', context)


@login_required(login_url='/accounts/login/')
def subscription_reg(request, slug):
    customer = request.user.customer
    restaurants = Restaurant.objects.all()
    item = Item.objects.filter(slug=slug, subcription_avail=True).first()

    offsite = Location.objects.filter(category="OffSite")  # offsite locations
    onsite = Location.objects.filter(category="OnSite")  # onsite locations
    pickup_location = Location.objects.get(
        category="Direct Pickup")  # direct pickup location

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        subscribe_date = timezone.now()  # getting current date
        # create a dictionary to store weekday as key and quantity interger number as value
        day_subscribed = {}
        if 'Monday' in request.POST and 'quantity1' in request.POST:
            quantity1 = request.POST.get("quantity1")
            day_subscribed[0] = quantity1

        if 'Tuesday' in request.POST and 'quantity2' in request.POST:
            quantity2 = request.POST.get("quantity2")
            day_subscribed[1] = quantity2

        if 'Wednesday' in request.POST and 'quantity3' in request.POST:
            quantity3 = request.POST.get("quantity3")
            day_subscribed[2] = quantity3

        if 'Thursday' in request.POST and 'quantity4' in request.POST:
            quantity4 = request.POST.get("quantity4")
            day_subscribed[3] = quantity4

        if 'Friday' in request.POST and 'quantity5' in request.POST:
            quantity5 = request.POST.get("quantity5")
            day_subscribed[4] = quantity5

        if 'Saturday' in request.POST and 'quantity6' in request.POST:
            quantity6 = request.POST.get("quantity6")
            day_subscribed[5] = quantity6

        if 'Sunday' in request.POST and 'quantity7' in request.POST:
            quantity7 = request.POST.get("quantity7")
            day_subscribed[6] = quantity7

        payment_method = request.POST.get("payment_method")
        delivery_time = request.POST.get("delivery_time")
        delivery_mode = request.POST.get("delivery_mode")
        location = request.POST.get("location")
        onsite_delivery_location = request.POST.get("onsite_location")
        offsite_delivery_location = request.POST.get("offsite_location")

        date = str(subscribe_date.date())

        # getting the weekday of the current date
        day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()

        ordered_dates = datetime.datetime.strptime(
            str(subscribe_date.date()), "%Y-%m-%d").date()  # getting todays date

        ordered_dates_dict = {}  # dictionary to store order dates and quantity
        # iterating through each keys which contains a list of weekdays and values which holds the quantity
        for key, value in day_subscribed.items():
            if key >= day:  # checks if weekdays in list is greater than eq to todays weekday
                # getting todays date till Sunday since this is a weekly subscription
                ordered_dates_modified = ordered_dates + \
                    timedelta(days=(key-day))
                day_ordered = datetime.datetime.strftime(
                    ordered_dates_modified, '%Y-%m-%d')
                # assignin the dictionary a key of dates ordered and the quantity values of day_subscribed dictionary
                ordered_dates_dict[day_ordered] = value

        # converting time string type to time type
        delivery_time_modified = datetime.datetime.strptime(
            str(delivery_time), "%H:%M").time()
        print(ordered_dates_dict)
        print(item.title)
        # print(offsite.name)

        for ordered_dates in ordered_dates_dict:  # loop through the dates for the days chosen
            # assigning quantity to the key at the dates
            quantity = ordered_dates_dict[ordered_dates]
            ordered_dates_modified = datetime.datetime.strptime(
                str(ordered_dates), "%Y-%m-%d").date()  # converting date string type to date type

            delivery_date_time = datetime.datetime.combine(
                ordered_dates_modified, delivery_time_modified)  # combining dates and the time entered in the html time form fields
            # create orders on those dates and adds the quantity orderdered
            subcription_order = OrderItems.objects.create(
                item=item, customer=customer, ordered_date=ordered_dates, delivery_date=delivery_date_time, delivery_mode=delivery_mode, status='Active', subscription_order=True, quantity=quantity)

        # number of days is equal to the length of dictionary
        number_days = len(ordered_dates_dict)
        mealsubcription = MealSubscription.objects.create(item=item, customer=customer,
                                                          days_available=ordered_dates_dict.keys(), payment_method=payment_method, time_ordered=delivery_time_modified, subscription_status=True, number_days=number_days)
        # after creating checks for payment method and location
        subscription_id = mealsubcription.id  # getting the subscription id
        items = OrderItems.objects.filter(
            customer=customer, status="Active", isPaid=False, subscription_order=True).order_by('-ordered_date')  # not yet been delivered
        subscription = MealSubscription.objects.filter(id=subscription_id)

        if delivery_mode == 'pickup':
            items.update(payment_method=payment_method,
                         delivery_mode=delivery_mode, delivery_location=pickup_location)
            subscription.update(delivery_mode=delivery_mode,
                                delivery_location=pickup_location)

        if delivery_mode == 'deliver' and location == 'onsite':
            location_on = Location.objects.get(
                id=onsite_delivery_location)  # get onsite location
            items.update(payment_method=payment_method,
                         delivery_mode=delivery_mode, delivery_location=location_on)
            subscription.update(delivery_mode=delivery_mode,
                                delivery_location=pickup_location)
           # print('Youre opting for onsite delivery')

        if delivery_mode == 'deliver' and location == 'offsite':
            location_off = Location.objects.get(
                id=offsite_delivery_location)  # get offsite location
            items.update(payment_method=payment_method,
                         delivery_mode=delivery_mode, delivery_location=location_off)
            subscription.update(delivery_mode=delivery_mode,
                                delivery_location=pickup_location)
           # print('Youre opting for offsite delivery')

        if request.POST.get("payment_method") == 'Debit/Credit Card':
            return redirect('stripepayment:index')  # redirect to stripe page

        messages.info(
            request, "You're now subscribed for {} meal".format(item.title))
        # redirect to a new URL:
        return redirect(f"/mealsubscription/subscribing/{item.slug}")

    # print(item.title)
    # print(offsite.name)
    context = {
        'item': item,
        'offsite': offsite,
        'onsite': onsite,
        'restaurants': restaurants,
    }
    return render(request, 'mealsubscription/subscription_reg.html', {'context': context})


class SubscriptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'mealsubscription/subscribeitems_confirm_delete.html'

    def get_success_url(self, *args, **kwargs):
        item_slug = self.object.item.slug
        return reverse_lazy('mealsubscription:subscribing', kwargs={'slug': item_slug})

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
