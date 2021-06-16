from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('customers', CustomerViewSet)
router.register('items', ItemViewSet)
router.register('mealsubscriptions', MealSubscriptionsViewSet)
router.register('orders', OrderItemsViewSet, basename='orders')
router.register('locations', LocationViewSet)
router.register('payrolls', PayrollViewSet)
router.register('menus', MenuViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
