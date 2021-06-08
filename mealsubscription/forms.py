from django import forms
from main.models import *
from .models import *
from django.utils import timezone
from django.forms import ModelChoiceField

'''
 class SubscriptionForm(forms.ModelForm):
    DELIVERY_MODE = (
           ('Delivered', 'Delivered'),
           ('Out for delivery', 'Out for delivery'),
           ('Pickup', 'Pickup')
       )
       PAYMENT_METHOD = (
           ('Payroll', 'Payroll'),
           ('Credit', 'Credit')
       )

       days_available = forms.IntegerField(default=1)
       time = forms.TimeField(auto_now=False, auto_now_add=False, null=True)
       delivery_mode = forms.ChoiceField(choices=DELIVERY_MODE)
       payment_method = forms.ModelChoiceField(choices=PAYMENT_METHOD)
       delivery_location = forms.ModelChoiceField(
           queryset=Location.objects.all(), initial=0)

     class Meta:
         model = MealSubscription
         fields = __all__

         fields = ('days_available', 'time', 'delivery_mode',
                   'payment_method', 'delivery_location')



     def save(self, commit=True):
         custtomer = Customer
         payroll = super(PayrollRegistrationForm, self).save(commit=False)
         payroll.employee_id = self.cleaned_data["employee_id"]
         payroll.name = self.cleaned_data["name"]
         payroll.birth_date = self.cleaned_data["birth_date"]
        # user.last_name = self.cleaned_data["last_name"]
         payroll.customer_acc = self.instance.customer
         if commit:

             payroll.save()
         return payroll
 '''
