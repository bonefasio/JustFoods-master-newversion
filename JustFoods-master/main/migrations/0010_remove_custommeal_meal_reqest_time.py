# Generated by Django 3.1.7 on 2021-05-28 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_item_hide_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custommeal',
            name='meal_reqest_time',
        ),
    ]
