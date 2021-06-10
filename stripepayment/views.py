from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from main.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = "sk_test_51ItkkfAh9WweYVQmHWWyufzm8D3teuWlZMwopwIA5egeYnKEYldtFLudJVZDNtpZU0G3quJLk4PcPhn2t6IJJRqV00j8aMhhut"

# Create your views here.


@login_required
def index(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=False, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity

    context = {
        'items': items,
        'total': total,
        'count': count
    }

    return render(request, 'stripepayment/index.html', context)


@login_required
def charge(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer,  ordered=False, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")  # order total
    count = number.get("quantity__sum")  # sum of quantity
    total = round(total)
    print(total)
    if request.method == 'POST':
        print('Data:', request.POST)
        # this code is taken from https://stripe.com/docs/
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=total*100,  # total is multuplied by 100 as amount is in cents
            currency='fjd',
            description="Total Paid for {} Dish".format(count)
        )

        ordered_date = timezone.now()  # assign ordred date the current date
        items.update(ordered=True, ordered_date=ordered_date, isPaid=True)
        messages.info(request, "Item Paid and Ordred")

    return redirect(reverse('stripepayment:pay-success'))


@login_required
def success(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active", isPaid=True).order_by('-ordered_date')  # not yet been delivered
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity

    context = {
        'items': items,
        'total': total,
        'count': count
    }

    return render(request, 'stripepayment/success.html', context)
