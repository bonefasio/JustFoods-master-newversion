from django.db import models
from main.models import *
# Create your models here.


class MealSubscription(models.Model):

    PAYMENT_METHOD = (
        ('Payroll', 'Payroll'),
        ('Credit', 'Credit')
    )

    DELIVERY_MODE = (
        ('Delivered', 'Delivered'),
        ('PickUp', 'PickUp')
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True)
    days_available = models.IntegerField(default=7)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    delivery_mode = models.CharField(max_length=30, choices=DELIVERY_MODE)
    delivery_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True)
    payment_method = models.CharField(
        max_length=30, choices=PAYMENT_METHOD, default='Credit')
   # subscribe_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Meal Subscription'
        verbose_name_plural = 'Meal Subscriptions'

    def __str__(self):
        return self.item.title
