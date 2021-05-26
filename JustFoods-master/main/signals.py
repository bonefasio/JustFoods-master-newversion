
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Customer, Payroll

'''
def customer_profile(sender, instance, created, **kwargs):
    if created:  # check if user is created
        group = Group.objects.get(name='customer')
        instance.groups.add(group)  # add user to cutomer group
        Customer.objects.create(  # create customer profile of the user
            user=instance,
            name=instance.username,
        )
        print('Profile created!')


post_save.connect(customer_profile, sender=User)

'''


def payroll_profile(sender, instance, created, **kwargs):
    if created:  # check if user is created
        Payroll.objects.create(customer_acc=instance)

        print('Payroll created!')


post_save.connect(payroll_profile, sender=Customer)
