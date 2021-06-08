from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Item, OrderItems, Reviews
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
from .decorators import *
from django.db.models import Sum
from .forms import PayrollRegistrationForm, SubscriptionForm, OrderItemForm
import datetime
from datetime import timedelta


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
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    customer = request.user.customer
    ordered_date = timezone.now()
    order_item = OrderItems.objects.create(
        item=item,
        customer=customer,
        ordered=False,
        ordered_date=ordered_date,
        subscription_order=False
    )
    order_item.save()
    messages.info(request, "Added to Cart!!Continue Shopping!!")
    return redirect("main:cart")


@login_required
def get_cart_items(request):
    customer = request.user.customer
    ordered_items = OrderItems.objects.filter(
        customer=customer, ordered=False, subscription_order=False)
    bill = ordered_items.aggregate(Sum('item__price'))
    number = ordered_items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    context = {
        'ordered_items': ordered_items,
        'total': total,
        'count': count,
    }
    return render(request, 'main/cart.html', context)


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'main/cartitems_confirm_delete.html'
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user.customer == cart.customer:
            return True
        return False


@login_required
def order_delivery(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered

    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity
    # count = OrderItems.objects.filter()
    offsite = Location.objects.filter(category="OffSite")  # offsite locations
    onsite = Location.objects.filter(category="OnSite")  # onsite locations
    pickup_location = Location.objects.get(
        category="Direct Pickup")  # direct pickup location

    if request.method == 'POST':
        payment_method = request.POST.get("payment_method")
        delivery_date = request.POST.get("delivery_date")
        delivery_mode = request.POST.get("delivery_mode")
        location = request.POST.get("location")
        onsite_delivery_location = request.POST.get("onsite_location")
        offsite_delivery_location = request.POST.get("offsite_location")

        print('Location')
        print(onsite_delivery_location)

        if delivery_mode == 'pickup':
            items.update(payment_method=payment_method, delivery_date=delivery_date,
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
        return redirect('main:payment-page')

    context = {
        'items': items,
        'total': total,
        'count': count,
        'offsite': offsite,
        'onsite': onsite
    }
    return render(request, 'main/order_delivery.html', context)


@login_required
def order_details(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active").order_by('-ordered_date')  # not yet been delivered
    order_items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Delivered", isPaid=True).order_by('-ordered_date')  # delivered and paid orders
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity
    # count = OrderItems.objects.filter()
    context = {
        'items': items,
        'order_items': order_items,  # Delivered Items
        'total': total,
        'count': count
    }
    return render(request, 'main/order_details.html', context)


@login_required
def payment(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, isPaid=False, status="Active").order_by('-ordered_date')  # not yet been delivered

    ordered_date = timezone.now()  # assign ordred date the current date
    items.update(ordered=True, ordered_date=ordered_date)

    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity
    # count = OrderItems.objects.filter()
    context = {
        'items': items,
        # 'order_items': order_items,  # Delivered Items
        'total': total,
        'count': count
    }
    return render(request, 'main/payment.html', context)


def payroll_reg(request):
    payroll = Payroll.objects.filter(
        customer_acc=request.user.customer)
    cust_instance = Customer.objects.filter(user=request.user)

    payroll_registered = Payroll.objects.filter(registered=True)

    if payroll_registered:
        cust_instance.update(registered_payroll=True)
        messages.info(request, "You are Registered for payroll")
        return redirect("main:payitems")
    # if this is a POST request we need to process the form data

    elif request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PayrollRegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            employee_id = form.cleaned_data["employee_id"]
            name = form.cleaned_data["name"]
            birth_date = form.cleaned_data["birth_date"]
            # payroll = form.save()
            payroll.update(name=name, employee_id=employee_id,
                           birth_date=birth_date, registered=True)

            cust_instance.update(registered_payroll=True)

            messages.info(request, "Registered for payroll")
            # redirect to a new URL:
            return redirect('main:payitems')
            # return HttpResponseRedirect('Registered for payroll')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PayrollRegistrationForm()

    return render(request, 'main/payroll_reg.html', {'form': form})


@login_required
def pay_item(request):
    customer = request.user.customer
    # collect all paid ordered items
    paiditems = OrderItems.objects.filter(
        customer=request.user.customer, ordered=True, isPaid=False, status="Active").order_by('-ordered_date')
    paidDate = timezone.now()
    ordered_date = timezone.now()  # assign ordred date the current date
    #items.update(ordered=True, ordered_date=ordered_date)
    paiditems.update(isPaid=True, paidAt=paidDate,
                     ordered=True, ordered_date=ordered_date)
   # order_items.update(ordered=True, ordered_date=ordered_date)
    messages.info(request, "Item Paid")
    return redirect("main:payment_details")


@login_required
def payment_details(request):

    payroll = Payroll.objects.filter(
        registered=True, customer_acc=request.user.customer).first()
    cust_instance = Customer.objects.filter(
        user=request.user, registered_payroll=True).first()
    # collects items that are paid
    items = OrderItems.objects.filter(
        customer=request.user.customer, ordered=True, isPaid=True, status="Active").order_by('-ordered_date')
    # delivered_items = OrderItems.objects.filter(
    # customer=request.user.customer, ordered=True, status="Delivered").order_by('-ordered_date')
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")

    # updating customer total order
    cust_instance.customer_order_total = total
    cust_instance.save()

    # getting the payroll account balance
    account_balance_obj = payroll._meta.get_field(
        'account_balance')
    payroll_acc = account_balance_obj.value_from_object(payroll)

    cust_total = cust_instance.customer_order_total

   # payroll_acc = payroll.account_balance

    if payroll and cust_instance:
        payroll_acc = payroll_acc - cust_instance.customer_order_total
        paidDate = timezone.now()
       # items.update(isPaid=True, paidAt=paidDate,
        #             status="Delivered")  # update order items
        # update customer total
       # cust_instance.customer_order_total = 0.00
       # cust_instance.save()
        payroll.account_balance = payroll_acc  # update payroll account
        payroll.save()

    else:
        messages.info(request, "You have not registered for payroll payment")
        return redirect("main:order_details")

    context = {
        'cust_total': cust_total,
        'count': count,
        'items': items,
        'payroll_acc': payroll_acc,
    }
    return render(request, 'main/payment_details.html', context)


@login_required
def delivery_details(request):
    customer = request.user.customer
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
        'count': count
    }
    return render(request, 'main/delivery_details.html', context)


@login_required
def lunch(request):
    menu = get_object_or_404(Menu, description="Lunch")
    #item = get_object_or_404(Item, slug=slug)

    items = menu.items.all()
    print(items)
    context = {
        'items': items,
    }
    return render(request, 'main/lunch.html', context)


@login_required
def dinner(request):
    menu = get_object_or_404(Menu, description="Dinner")
    # get all items in menu
    items = menu.items.all()
    context = {
        'items': items,
    }
    return render(request, 'main/dinner.html', context)


@login_required
def breakfast(request):
    menu = get_object_or_404(Menu, description="Breakfast")
    # get all items in menu
    items = menu.items.all()
    print(items)

    context = {
        'items': items,
    }
    return render(request, 'main/breakfast.html', context)


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'main/orderitems_confirm_delete.html'
    success_url = '/order_delivery'

    def test_func(self):
        subscribing = self.get_object()
        if self.request.user.customer == subscribing.customer:
            return True
        return False
