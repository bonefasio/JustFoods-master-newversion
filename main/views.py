from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Item, OrderItems, Reviews, CustomMeal
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


class MenuListView(ListView):
    model = Item
    template_name = 'main/home.html'
    context_object_name = 'menu_items'


def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7]
    avail = int(item.quantity_available)
    loop_times = range(1, avail+1)
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


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'image', 'description', 'price',
              'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'image', 'description', 'price',
              'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/item_list'

    def test_func(self):
        item = self.get_object()
        if self.request.user.customer == item.created_by:
            return True
        return False


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
    # pieces = cart_items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    # total_pieces = pieces.get("item__pieces__sum")
    context = {
        'ordered_items': ordered_items,
        'total': total,
        'count': count,
        # 'total_pieces': total_pieces
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
def order_item(request):
    customer = request.user.customer
    order_items = OrderItems.objects.filter(customer=customer, ordered=False)
    ordered_date = timezone.now()
    order_items.update(ordered=True, ordered_date=ordered_date)
    messages.info(request, "Item Ordered")
    return redirect("main:order_delivery")


@login_required
def order_delivery(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered
   # order_items = OrderItems.objects.filter(
    # customer=customer, ordered=True, status="Delivered", isPaid=True).order_by('-ordered_date')  # delivered and paid orders
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity
    # count = OrderItems.objects.filter()
    offsite = OffSiteLocation.objects.all()
    onsite = OnSiteLocation.objects.all()

    if request.method == 'POST':
        payment_method = request.POST.get("payment_method")
        delivery_date = request.POST.get("delivery_date")
        delivery_mode = request.POST.get("delivery_mode")
        location = request.POST.get("location")
        onsite_delivery_location = request.POST.get("onsite_location")
        offsite_delivery_location = request.POST.get("offsite_location")

        print(payment_method, delivery_date,  delivery_mode, location,
              onsite_delivery_location, offsite_delivery_location)
        # string = "freeCodeCamp"
        onsitelocation_string = onsite_delivery_location[0:7]
        offsitelocation_string = offsite_delivery_location[0:7]

        if request.POST.get("delivery_mode") == 'pickup':
            field_name = 'pickup_location'
            obj = Location.objects.first()
            field_object = Location._meta.get_field(field_name)
            field_value = getattr(obj, field_object.attname)
            print('Pickup from Cafeteria')
            items.update(payment_method=payment_method, delivery_date=delivery_date,
                         delivery_mode=delivery_mode, delivery_location=field_value)

        if request.POST.get("delivery_mode") == 'Delivery' and request.POST.get("location") == 'onsite':

            onsitelocation = OnSiteLocation.objects.filter(
                name__contains=onsitelocation_string)
            location = Location.objects.filter(onsite=onsitelocation)
            items.update(payment_method=payment_method, delivery_date=delivery_date,
                         delivery_mode=delivery_mode, delivery_location=location)
            print('Youre opting for onsite delivery')

        if request.POST.get("delivery_mode") == 'Delivery' and request.POST.get("location") == 'offsite':

            offsitelocation = OffSiteLocation.objects.filter(
                name__contains=offsitelocation_string)
            location = Location.objects.filter(onsite=offsitelocation)
            items.update(payment_method=payment_method, delivery_date=delivery_date,
                         delivery_mode=delivery_mode, delivery_location=location)
            print('Youre opting for offsite delivery')

        if request.POST.get("payment_method") == 'Debit/Credit Card':
            return redirect('main:payment_paypal')

        messages.info(request, "Delivery details saved")
        # redirect to a new URL:
        return redirect('main:payment-page')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderItemForm()

    context = {
        'items': items,
        # 'order_items': order_items,  # Delivered Items
        'total': total,
        'count': count,
        'form': form,
        'offsite': offsite,
        'onsite': onsite
    }
    return render(request, 'main/order_delivery.html', context)


@login_required
def payment_paypal(request):
    customer = request.user.customer
    items = OrderItems.objects.filter(
        customer=customer, ordered=True, status="Active", isPaid=False).order_by('-ordered_date')  # not yet been delivered
   # order_items = OrderItems.objects.filter(
    # customer=customer, ordered=True, status="Delivered", isPaid=True).order_by('-ordered_date')  # delivered and paid orders
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")  # sum of quantity

    context = {
        'items': items,
        # 'order_items': order_items,  # Delivered Items
        'total': total,
        'count': count
    }
    return render(request, 'main/payment_paypal.html', context)


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
    # order_items = OrderItems.objects.filter(
    #  customer=customer, ordered=True, status="Delivered", isPaid=False).order_by('-ordered_date')  # delivered and paid orders
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
    paiditems.update(isPaid=True, paidAt=paidDate)
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
    lunch = OrderItems.objects.filter(item__meal_menu="Lunch")

    context = {
        'lunch': lunch,
    }
    return render(request, 'main/lunch.html', context)


@login_required
def dinner(request):
    dinner = OrderItems.objects.filter(item__meal_menu="Dinner")

    context = {
        'dinner': dinner,
    }
    return render(request, 'main/dinner.html', context)


@login_required
def breakfast(request):
    breakfast = OrderItems.objects.filter(item__meal_menu="Breakfast")

    context = {
        'breakfast': breakfast,
    }
    return render(request, 'main/breakfast.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def admin_view(request):
    cart_items = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'main/admin_view.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    context = {
        'items': items
    }
    return render(request, 'main/item_list.html', context)


@login_required
@admin_only
def update_status(request, pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, status="Active", pk=pk)
    delivery_date = timezone.now()
    if status == 'Delivered':
        cart_items.update(
            status=status, delivery_date=delivery_date, isDelivered=True)
    return render(request, 'main/pending_orders.html')


@login_required(login_url='/accounts/login/')
@admin_only
def pending_orders(request):
    items = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, status="Active").order_by('-ordered_date')
    context = {
        'items': items,
    }
    return render(request, 'main/pending_orders.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def admin_dashboard(request):
    cart_items = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True)
    pending_total = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, status="Active").count()
    completed_total = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, status="Delivered").count()
    count1 = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, item="3").count()
    count2 = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, item="4").count()
    count3 = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, item="5").count()
    total = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True).aggregate(Sum('item__price'))
    income = total.get("item__price__sum")
    context = {
        'pending_total': pending_total,
        'completed_total': completed_total,
        'income': income,
        'count1': count1,
        'count2': count2,
        'count3': count3,
    }
    return render(request, 'main/admin_dashboard.html', context)


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
    return render(request, 'main/subscription.html', context)


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
            days_available_newlist = []
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
            return redirect(f"/subscribing/{item.slug}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscriptionForm()

    return render(request, 'main/subscription_reg.html', {'form': form})


class SubscriptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'main/subscribeitems_confirm_delete.html'

    def get_success_url(self, *args, **kwargs):
        item_slug = self.object.item.slug
        return reverse_lazy('main:subscribing', kwargs={'slug': item_slug})

    def test_func(self):
        subscribing = self.get_object()
        if self.request.user.customer == subscribing.customer:
            return True
        return False


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItems
    template_name = 'main/orderitems_confirm_delete.html'
    success_url = '/order_delivery'

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
        meal_reqest_time = request.POST.get("meal_reqest_time")
        meal_reqest_date = request.POST.get("meal_reqest_date")
        order_quantity = request.POST.get("order_quantity")
        custom_meal_receipe = request.POST.get("custom_meal_receipe")
        custom_meal_ingredients = request.POST.get("custom_meal_ingredients")

        custom_meal = CustomMeal(custom_meal_name=custom_meal_name, patron_first_name=patron_first_name,
                                 patron_last_name=patron_last_name,
                                 patron_email_address=patron_email_address,
                                 patron_phone_contact=patron_phone_contact, meal_reqest_time=meal_reqest_time,
                                 meal_reqest_date=meal_reqest_date, order_quantity=order_quantity,
                                 custom_meal_receipe=custom_meal_receipe,
                                 custom_meal_ingredients=custom_meal_ingredients)
        custom_meal.save()
        messages.success(
            request, "Custom Meal Request Sent, Kindly Wait For Cafeteria Response!!")
    return render(request, 'main/custom_meal.html')
