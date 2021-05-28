from django.contrib import admin
# Item, OrderItems, Reviews, Customer, Payroll, MealSubscription, Location, CustomMeal
from .models import *
from django.db import models


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Created By", {'fields': ["created_by"]}),
        ("Title", {'fields': ["title"]}),
        ("Image", {'fields': ["image"]}),
        ("Description", {'fields': ["description"]}),
        ("Price", {'fields': ["price"]}),
        ("Instructions", {'fields': ["instructions"]}),
        ("Labels", {'fields': ["labels"]}),
        ("Label Colour", {'fields': ["label_colour"]}),
        ("Slug", {'fields': ["slug"]}),
        ("Quantity", {'fields': ["quantity_available"]}),
        ("Menu Type", {'fields': ["meal_menu"]}),
        ("Subscription Status", {'fields': ["subcription_avail"]}),
        ("Hide Menu", {'fields': ["hide_menu"]}),

    ]
    list_display = ('id', 'created_by', 'title', 'description',
                    'price', 'labels', 'quantity_available')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'user', 'date_created', 'phone', 'employee_id',
                    'registered_payroll', 'customer_order_total')


class PayrollAdmin(admin.ModelAdmin):
    list_display = ('id','customer_acc', 'account_balance',
                    'created_time', 'registered')


class OrderItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Order Status", {'fields': ["status"]}),
        ("Delivery Date", {'fields': ["delivery_date"]}),

    ]
    list_display = ('id', 'customer', 'item', 'quantity',
                    'ordered', 'ordered_date', 'delivery_date', 'status', 'isPaid', 'paidAt', 'isDelivered', 'delivery_mode', 'delivery_location', 'subscription_order')
    list_filter = ('ordered', 'ordered_date', 'status')


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'item', 'review', 'posted_on')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'category')
    list_filter = ('category', 'name')


class MealSubscriptionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Items", {'fields': ["item"]}),
        ("Customer", {'fields': ["customer"]}),
        ("Days", {'fields': ["days_available"]}),
        ("Time", {'fields': ["time_ordered"]}),
        ("Delivery Method", {'fields': ["delivery_mode"]}),
        ("Location Deliver", {'fields': ["delivery_location"]}),
        ("Payment Method", {'fields': ["payment_method"]}),
        ("Order Status", {'fields': ["status"]}),
    ]
    list_display = ('id','time_ordered', 'item', 'customer', 'days_available',
                    'delivery_mode', 'payment_method', 'number_days','status')

# custom meal code below
class CustomMealAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Custom Meal Name", {'fields': ["custom_meal_name"]}),
        ("Patron First Name", {'fields': ["patron_first_name"]}),
        ("Patron Last Name", {'fields': ["patron_last_name"]}),
        ("Patron Email Address", {'fields': ["patron_email_address"]}),
        ("Patron Phone Contact", {'fields': ["patron_phone_contact"]}),
        ("Meal Request Time", {'fields': ["meal_reqest_time"]}),
        ("Meal Request Date", {'fields': ["meal_reqest_date"]}),
        ("Order Quantity", {'fields': ["order_quantity"]}),
        ("Custom Meal Receipe", {'fields': ["custom_meal_receipe"]}),
        ("Custom Meal Ingredients", {'fields': ["custom_meal_ingredients"]}),
        ("Order Status", {'fields': ["request_order_status"]}),
        ("Custom Meal Price", {'fields': ["custom_meal_price"]}),
    ]
    list_display = ('id','custom_meal_name', 'patron_first_name', 'patron_last_name',
                    'meal_reqest_time', 'meal_reqest_date', 'order_quantity', 'custom_meal_receipe',
                    'custom_meal_ingredients', 'request_order_status', 'custom_meal_price')

class InventoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Item Name", {'fields': ["item_name"]}),
        ("Item Purchase Date", {'fields': ["item_purchase_date"]}),
        ("Item Purchase Expirydate", {'fields': ["item_purchase_expirydate"]}),
        ("Item Quantity Available", {'fields': ["item_quantity_available"]}),
        ("Item Purchase Price", {'fields': ["item_purchase_price"]}),
    ]
    list_display = ('id', 'item_name', 'item_purchase_date', 'item_purchase_expirydate',
                    'item_quantity_available', 'item_purchase_price')

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(MealSubscription, MealSubscriptionAdmin)
# custom meal register below
admin.site.register(CustomMeal, CustomMealAdmin)
# inventory meal
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Location, LocationAdmin)
