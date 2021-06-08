from django.shortcuts import render
from django.urls import reverse_lazy
from main.models import *
#from main.models import MealSubscription
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
from main.forms import SubscriptionForm
from datetime import timedelta
# Create your views here.


@login_required(login_url='/accounts/login/')
def subscriptionDetail(request, slug):
    customer = request.user.customer
    item = Item.objects.filter(slug=slug, subcription_avail=True).first()
    subscription_ordered_items = OrderItems.objects.filter(
        item=item, customer=customer, subscription_order=True)

    # avail = int(item.quantity_available)
   # days = int(subscription.days_available)

    # loop_times_avail = range(1, avail+1)
   # loop_times_days = range(1, avail+1)
    context = {
        'item': item,
        'subscription_ordered_items': subscription_ordered_items,
        # 'loop_times_days': loop_times_days,
        # 'avail': avail,
        # 'days': days,
    }
    return render(request, 'mealsubscription/subscription.html', context)


@login_required(login_url='/accounts/login/')
def subscription_reg(request, slug):
    customer = request.user.customer
    item = Item.objects.filter(slug=slug, subcription_avail=True).first()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subscribe_date = timezone.now()
            # process the data in form.cleaned_data as required
            days_available = form.cleaned_data["days_available"]
            time_ordered = form.cleaned_data["time_field"]
            delivery_mode = form.cleaned_data["delivery_mode"]
            payment_method = form.cleaned_data["payment_method"]
            delivery_location = form.cleaned_data["delivery_location"]

            date = str(subscribe_date.date())
            day_name = ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']
            # getting the weekday of the current date
            day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
          # print(day_name[day])
           # print(day)
            print(days_available)
           # days_available_newlist = []
            day_subscribed = []  # list of days available for subscription
            for days in days_available:
                if days == 'Monday':
                    day_subscribed.append(0)
                if days == 'Tuesday':
                    day_subscribed.append(1)
                if days == 'Wednesday':
                    day_subscribed.append(2)
                if days == 'Thursday':
                    day_subscribed.append(3)
                if days == 'Friday':
                    day_subscribed.append(4)
                if days == 'Saturday':
                    day_subscribed.append(5)
                if days == 'Sunday':
                    day_subscribed.append(6)

            ordered_dates = datetime.datetime.strptime(
                str(subscribe_date.date()), "%Y-%m-%d").date()  # getting todays date

            ordered_dates_list = []
            for weekdays in day_subscribed:
                if weekdays >= day:  # checks if weekdays in list is greater than eq to todays weekday
                    ordered_dates_modified = ordered_dates + \
                        timedelta(days=(weekdays-day))
                    day_ordered = datetime.datetime.strftime(
                        ordered_dates_modified, '%Y-%m-%d')
                    ordered_dates_list.append(day_ordered)

            for ordered_dates in ordered_dates_list:  # loop through the dates for the days chosen
                subcription_order = OrderItems.objects.create(
                    item=item, customer=customer, delivery_location=delivery_location, ordered_date=ordered_dates, delivery_mode=delivery_mode, isPaid=False, isDelivered=False, status='Active', subscription_order=True)

            number_days = len(ordered_dates_list)  # number of days

            mealsubcription = MealSubscription.objects.create(item=item, customer=customer,
                                                              days_available=ordered_dates_list, time_ordered=time_ordered, delivery_mode=delivery_mode, payment_method=payment_method, delivery_location=delivery_location, subscription_status=True, number_days=number_days)

            messages.info(
                request, "You're now subscribed for {} meal".format(item.title))
            # redirect to a new URL:
            # return reverse('main:subscribing', kwargs={'slug': item.slug})
            return redirect(f"/mealsubscription/subscribing/{item.slug}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscriptionForm()

    return render(request, 'mealsubscription/subscription_reg.html', {'form': form})


class SubscriptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'mealsubscription/subscribeitems_confirm_delete.html'

    def get_success_url(self, *args, **kwargs):
        item_slug = self.object.item.slug
        return reverse_lazy('mealsubscription:subscribing', kwargs={'slug': item_slug})

    def test_func(self):
        subscribing = self.get_object()
        if self.request.user.customer == subscribing.customer:
            return True
        return False

# custom meal


@login_required
def custom_meal(request):
    if request.method == "POST":
        custom_meal_name = request.POST.get("custom_meal_name")
        patron_first_name = request.POST.get("patron_first_name")
        patron_last_name = request.POST.get("patron_last_name")
        patron_email_address = request.POST.get("patron_email_address")
        patron_phone_contact = request.POST.get("patron_phone_contact")
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
    return render(request, 'mealsubscription/custom_meal.html')
