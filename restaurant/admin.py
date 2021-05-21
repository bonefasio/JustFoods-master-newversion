from django.contrib import admin
from restaurant.models import *
# Register your models here.


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('place', 'serves_hot_dogs', 'serves_pizza')


admin.site.register(Place, PlaceAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
