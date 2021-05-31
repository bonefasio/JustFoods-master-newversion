from django.db import models
from django.conf import settings
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ManyToManyField
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from multiselectfield import MultiSelectField


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200, null=True)
    # profile_pic = models.ImageField(default="profile1.png", null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    customer_order_total = models.FloatField(
        null=True, blank=True, default=12.3)
    employee_id = models.CharField(max_length=50, default=12.3)
    registered_payroll = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Payroll(models.Model):
    customer_acc = models.OneToOneField(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    account_balance = models.FloatField(null=True, blank=True, default=134.34)
    name = models.CharField(max_length=200, null=True)
    registered = models.BooleanField(default=False)
    employee_id = models.CharField(max_length=200, null=True)
    birth_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Payroll'
    '''
    def __str__(self):
        return self.customer_acc.name
    '''


class Item(models.Model):
    LABELS = (
        ('BestSeller', 'BestSeller'),
        ('New', 'New'),
        ('Spicy🔥', 'Spicy🔥'),
        ('Veggies', 'Veggies')
    )
    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info')
    )

    DELIVERY_CHOICE = (
        ('Pickup', 'Pickup'),
        ('Delivery Available', 'Delivery Available'),
        ('Both Available [Pickup & Delivery Available]',
         'Both Available [Pickup & Delivery Available]')
    )
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True)
    price = models.FloatField()
    instructions = models.CharField(
        max_length=250, choices=DELIVERY_CHOICE, blank=True)
    image = models.ImageField(default='default.png', upload_to='images/')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(
        max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(max_length=255, default="slug")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=1)
    subcription_avail = models.BooleanField(default=False)

    # restaurants = models.ForeignKey(Restaurant, on_delete = models.CASCADE,blank=True)
    class Meta:
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:dishes", kwargs={
            'slug': self.slug
        })

    def get_add_to_order_url(self):  # get_add_to_cart_url
        return reverse("main:add-to-order", kwargs={
            'slug': self.slug
        })

    def get_item_delete_url(self):
        return reverse("main:item-delete", kwargs={
            'slug': self.slug
        })

    def get_update_item_url(self):
        return reverse("main:item-update", kwargs={
            'slug': self.slug
        })


class Menu(models.Model):
    MENU_TYPE = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Display', 'Display'),
        ('Hide', 'Hide')
    )
    items = models.ManyToManyField(Item)
    description = models.CharField(
        max_length=25, choices=MENU_TYPE, blank=True)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.description


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rslug = models.SlugField(max_length=255)
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review


class Location(models.Model):
    DELIVERY_LOCATION = (
        ('OnSite', 'OnSite'),
        ('OffSite', 'OffSite'),
        ('Direct Pickup', 'Direct Pickup')
    )
    name = models.CharField(max_length=50, default='USP', blank=True)
    address = models.CharField(max_length=80, blank=True)
    category = models.CharField(
        max_length=255, default='OnSite', choices=DELIVERY_LOCATION)

    def __str__(self):
        return "%s the place to deliver" % self.name


class OrderItems(models.Model):
    ORDER_STATUS = (
        ('Incomplete', 'Incomplete'),
        ('Accepted', 'Accepted'),
        ('Prepared', 'Prepared'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    )
    PAYMENT_METHOD = (
        ('Payroll', 'Payroll'),
        ('Credit/Debit Card', 'Credit/Debit Card')
    )
    DELIVERY_MODE = (
        ('Delivered (On Site Campus)', 'Delivered (On Site Campus)'),
        ('Delivered (Off Site Campus) *limited sites',
         'Delivered (Off Site Campus) *limited sites'),
        ('PickUp', 'PickUp')
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    delivery_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(
        auto_now_add=False, null=False, blank=False)
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_METHOD, default='Credit')
    status = models.CharField(
        max_length=255, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    delivery_mode = models.CharField(max_length=255, choices=DELIVERY_MODE)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    subscription_order = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Food Order Item'
        verbose_name_plural = 'Food Order Items'

    def __str__(self):
        return self.status

    def get_remove_from_order_url(self):  # get_remove_from_cart_url
        return reverse("main:remove-from-order", kwargs={  # remove-from-cart
            'pk': self.pk
        })

    def update_status_url(self):
        return reverse("main:update_status", kwargs={
            'pk': self.pk
        })


class MealSubscription(models.Model):
    ORDER_STATUS = (
        ('Incomplete', 'Incomplete'),
        ('Accepted', 'Accepted'),
        ('Prepared', 'Prepared'),
        ('Pending Delivery', 'Pending Delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    )
    PAYMENT_METHOD = (
        ('Payroll', 'Payroll'),
        ('Credit', 'Credit')
    )
    DELIVERY_MODE = (
        ('Delivered (On Site Campus)', 'Delivered (On Site Campus)'),
        ('Delivered (Off Site Campus) *limited sites',
         'Delivered (Off Site Campus) *limited sites'),
        ('PickUp', 'PickUp')
    )
    DAYS = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday")
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True)
    days_available = MultiSelectField(max_length=255, choices=DAYS)
    time_ordered = models.TimeField(
        auto_now=False, auto_now_add=False, null=True)
    delivery_mode = models.CharField(max_length=255, choices=DELIVERY_MODE)
    delivery_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True)
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_METHOD, default='Credit')
    subscription_status = models.BooleanField(default=False)
    number_days = models.IntegerField(default=1)
    status = models.CharField(
        max_length=255, choices=ORDER_STATUS, default='Active')

    class Meta:
        verbose_name = 'Meal Subscription'
        verbose_name_plural = 'Meal Subscriptions'

    def __str__(self):
        return self.delivery_mode


class CustomMeal(models.Model):
    ORDER_STATUS = (
        ('Incomplete', 'Incomplete'),
        ('Accepted', 'Accepted'),
        ('Prepared', 'Prepared'),
        ('Pending Delivery', 'Pending Delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    )
    custom_meal_name = models.CharField(max_length=150)
    patron_first_name = models.CharField(max_length=150)
    patron_last_name = models.CharField(max_length=150)
    patron_email_address = models.CharField(max_length=50)
    patron_phone_contact = models.CharField(max_length=50)
    meal_request_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    order_quantity = models.IntegerField(default=0)
    custom_meal_receipe = models.CharField(max_length=100)
    custom_meal_ingredients = models.CharField(max_length=100)
    request_order_status = models.CharField(
        max_length=255, choices=ORDER_STATUS, default='Pending')
    custom_meal_price = models.FloatField(default=False)

    class Meta:
        verbose_name = 'Custom Meal Order'
        verbose_name_plural = 'Custom Meal Orders'

    def __str__(self):
        return self.custom_meal_name


class Inventory(models.Model):
    item_name = models.CharField(max_length=150)
    item_purchase_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    item_purchase_expirydate = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    item_quantity_available = models.IntegerField(default=0)
    item_purchase_price = models.FloatField(default=False)

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'

    def __str__(self):
        return self.item_name
