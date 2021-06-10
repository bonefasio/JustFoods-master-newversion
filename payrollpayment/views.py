from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
#from django.urls import reverse_lazy
from main.models import Item, OrderItems, Reviews
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.decorators import *
from django.db.models import Sum
from main.forms import PayrollRegistrationForm

# Create your views here.


@login_required
def payroll_reg(request):
    payroll = Payroll.objects.filter(
        customer_acc=request.user.customer)
    cust_instance = Customer.objects.filter(user=request.user)

    payroll_registered = Payroll.objects.filter(registered=True)

    if payroll_registered:
        cust_instance.update(registered_payroll=True)
        messages.info(request, "You are Registered for payroll")
        return redirect("payrollpayment:payitems")
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
            return redirect('payrollpayment:payitems')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PayrollRegistrationForm()

    return render(request, 'payrollpayment/payroll_reg.html', {'form': form})


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
    return redirect("payrollpayment:payment_details")


@login_required
def payment(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, isPaid=False, status="Active").order_by('-ordered_date')  # not yet been delivered

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
    return render(request, 'payrollpayment/payment.html', context)


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
        return redirect("orders:order_details")

    context = {
        'cust_total': cust_total,
        'count': count,
        'items': items,
        'payroll_acc': payroll_acc
    }
    return render(request, 'payrollpayment/payment_details.html', context)
