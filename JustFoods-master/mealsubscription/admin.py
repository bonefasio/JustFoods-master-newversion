from django.contrib import admin
# Item, OrderItems, Reviews, Customer, Payroll, MealSubscription, Location
from .models import *
from django.db import models
# Register your models here.


class MealSubscriptionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Item", {'fields': ["customer"]}),
        ("Item", {'fields': ["item"]}),
        ("Time", {'fields': ["time"]}),
        ("Delivery Method", {'fields': ["delivery_mode"]}),
        ("Location Deliver", {'fields': ["delivery_location"]}),
        ("Payment Method", {'fields': ["payment_method"]}),

    ]
    list_display = ('time', 'customer', 'days_available',
                    'delivery_mode', 'payment_method')


admin.site.register(MealSubscription, MealSubscriptionAdmin)
