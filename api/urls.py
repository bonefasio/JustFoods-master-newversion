from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('customers', CustomerViewSet, basename='patrons')
router.register('items', ItemViewSet, basename='items')
router.register('mealsubscriptions', MealSubscriptionsViewSet,
                basename='mealsubscriptions')
router.register('orders', OrderItemsViewSet, basename='orders')
router.register('locations', LocationViewSet, basename='locations')
router.register('payrolls', PayrollViewSet, basename='payrolls')
router.register('menus', MenuViewSet, basename='menus')
router.register('place', PlaceViewSet, basename='place')
router.register('restaurant', RestaurantViewSet, basename='restaurant')


urlpatterns = [
    path('', include(router.urls)),
]
