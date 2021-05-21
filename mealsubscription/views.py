from django.shortcuts import render
from main.models import *
from .models import MealSubscription
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.decorators import *
from django.db.models import Sum
#from .forms import PayrollRegistrationForm
# Create your views here.


def subscriptionDetail(request, slug):
    customer = request.user.customer
    item = Item.objects.filter(slug=slug, subcription_avail=True).first()
   # orderitem = OrderItems.objects.create(item=item, customer=customer)
    subscription = MealSubscription.objects.create(
        item=item, customer=customer)

    avail = int(item.quantity_available)
    days = int(subscription.days_available)

    loop_times_avail = range(1, avail+1)
    loop_times_days = range(1, avail+1)
    context = {
        'item': item,
        # 'orderitem': orderitem,
        'loop_times_days': loop_times_days,
        'avail': avail,
        'days': days,
    }
    return render(request, 'mealsubscritption/subscription.html', context)


@login_required
def add_subscription(request):
    if request.method == "POST":
        customer = request.user.customer
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        orderitem = OrderItems.objects.filter(item=item, customer=customer)

        subscriptions = Reviews(
            customer=customer, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thankyou for subscribing to this product!!")
    return redirect(f"/subscription/{item.slug}")


def subscription_reg(request, slug):
    customer = request.user.customer
    item = Item.objects.filter(slug=slug, subcription_avail=True).first()
    orderitem = OrderItems.objects.create(item=item, customer=customer)
    subscription = MealSubscription.objects.create(
        item=item, customer=customer)
    mealsubcription = MealSubscription.objects.create(
        customer=request.user.customer, item=item)

    # if this is a POST request we need to process the form data '''

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            days_available = form.cleaned_data["days_available"]
            time = form.cleaned_data["time"]
            delivery_mode = form.cleaned_data["delivery_mode"]
            payment_method = form.cleaned_data["payment_method"]
            delivery_location = form.cleaned_data["delivery_location"]
            # payroll = form.save()
            subscription.update(days_available=days_available, time=time,
                                delivery_mode=delivery_mode, payment_method=payment_method, delivery_location=delivery_location)

            # cust_instance.update(registered_payroll=True)
            # payroll.update
            messages.info(request, "You're now subscribed for this meal")
            # redirect to a new URL:
            return redirect('mealsubscritption:subscribing')
            # return HttpResponseRedirect('Registered for payroll')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PayrollRegistrationForm()

    return render(request, 'mealsubscription/subscription_reg.html', {'form': form})
