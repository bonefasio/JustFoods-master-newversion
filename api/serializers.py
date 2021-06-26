from rest_framework import serializers
from main.models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'name', 'phone', 'date_created',
                  'registered_payroll', 'employee_id')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'price', 'instructions',
                  'slug', 'subcription_avail', 'quantity_available')


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ('id', 'customer_acc', 'account_balance', 'name',
                  'registered', 'employee_id', 'birth_date')


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('id', 'customer_acc', 'item', 'delivery_location',
                  'ordered', 'quantity', 'ordered_date', 'payment_method', 'status', 'delivery_date', 'delivery_mode', 'isPaid', 'paidAt', 'isDelivered', 'subscription_order')


class MealSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealSubscription
        fields = ('id', 'customer', 'item', 'delivery_location',
                  'days_available', 'time_ordered', 'payment_method', 'status', 'subscription_status', 'delivery_mode', 'delivery_location', 'number_days')


class CustomMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMeal
        fields = ('id', 'custom_meal_name', 'patron_first_name', 'patron_first_name',
                  'patron_last_name', 'patron_phone_contact', 'meal_request_date', 'meal_reqest_time', 'order_quantity', 'custom_meal_receipe', 'delivery_location', 'custom_meal_ingredients', 'request_order_status', 'custom_meal_price')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'category')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'items', 'description')


class RestaurantSerializer(serializers.ModelSerializer):
    #place = PlaceSerializer(many=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'place')


class PlaceSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'restaurants')
