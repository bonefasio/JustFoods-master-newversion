from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUSerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=10)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True, min_length=9, max_length=10)
   # employee_id = forms.CharField(required=True)
    #location = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "first_name",
                  "last_name", "password1", "password2")

class InternationalStudentForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=10)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True, min_length=11, max_length=12)
   # employee_id = forms.CharField(required=True)
    #location = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "email",  "first_name",
                  "last_name", "password1", "password2")
      
'''
    def save(self, commit=True):
        user = super(NewUSerForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
'''
