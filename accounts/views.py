from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import NewUSerForm, InternationalStudentForm
from django.contrib.auth.models import Group
from main.models import Customer, Payroll

def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)  # add user to cutomer group
            Customer.objects.create(  # create customer profile of the user
                user=user,
                name=user.username,
            )
            customer = Customer.objects.get(user=user)
            # create a payroll acount for that same user
            Payroll.objects.create(customer_acc=customer, registered=False)
            print('Profile created!')
            login(request, user)
            return redirect('main:home')
    else:
        form = NewUSerForm()
    # return render(request, 'accounts/signup.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': form})

def signupinternational_view(request):
    if request.method == 'POST':
        form = InternationalStudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)  # add user to cutomer group
            Customer.objects.create(  # create customer profile of the user
                user=user,
                name=user.username,
            )
            customer = Customer.objects.get(user=user)
            # create a payroll acount for that same user
            Payroll.objects.create(customer_acc=customer, registered=False)
            print('Profile created!')
            login(request, user)
            return redirect('main:home')
    else:
        form = InternationalStudentForm()
    # return render(request, 'accounts/signup.html', {'form': form})
    return render(request, 'accounts/internationalregister.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
    else:
        form = AuthenticationForm()
   # return render(request, 'accounts/login.html', {'form': form})
    return render(request, 'accounts/logintest.html', {'form': form})

def internationallogin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
    else:
        form = AuthenticationForm()
   # return render(request, 'accounts/login.html', {'form': form})
    return render(request, 'accounts/internationallogin.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
