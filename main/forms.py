
from django import forms
from .models import *  # Item, Customer, Payroll
from django.utils import timezone
from django.forms import ModelChoiceField
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

'''
class AddForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('created_by',
        'title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug')

'''


class PayrollRegistrationForm(forms.ModelForm):
    employee_id = forms.CharField(required=True)
    name = forms.CharField(required=True)
    birth_date = forms.DateTimeField(required=True)

    class Meta:
        model = Payroll
        fields = ('employee_id', 'name', 'birth_date')


class SubscriptionForm(forms.ModelForm):
    time_field = forms.TimeField(
        widget=TimePicker(
            options={
                'enabledHours': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                'defaultDate': '1970-01-01T14:56:00'
            },
            attrs={
                'input_toggle': True,
                'input_group': False,
                'type': 'time',
                'placeholder': 'Select time'
            },
        ),
    )

    class Meta:
        model = MealSubscription
        fields = ('days_available', 'time_field')
        # fields = ('days_available', 'time_field', 'delivery_mode',
        # 'payment_method', 'delivery_location')


class OrderItemForm(forms.ModelForm):
    delivery_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = OrderItems
        fields = ('payment_method', 'delivery_date',
                  'delivery_mode', 'delivery_location')
