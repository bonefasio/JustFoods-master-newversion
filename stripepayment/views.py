from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from main.models import *
from django.db.models import Sum

import stripe

stripe.api_key = "sk_test_51ItkkfAh9WweYVQmHWWyufzm8D3teuWlZMwopwIA5egeYnKEYldtFLudJVZDNtpZU0G3quJLk4PcPhn2t6IJJRqV00j8aMhhut"

# Create your views here.


def index(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered
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


def charge(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered
   # order_items = OrderItems.objects.filter(
    # customer=customer, ordered=True, status="Delivered", isPaid=True).order_by('-ordered_date')  # delivered and paid orders
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity
    total = round(total)
    print(total)
    if request.method == 'POST':
        print('Data:', request.POST)

       # amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=total*100,
            currency='fjd',
            description="Total Paid for {} Dish".format(count)
        )

    return redirect(reverse('stripepayment:success'))


def successMsg(request):

    return render(request, 'stripepayment/success.html')
