# Generated by Django 3.1.7 on 2021-06-04 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20210530_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='payment_method',
            field=models.CharField(choices=[('Payroll', 'Payroll'), ('Credit/Debit Card', 'Credit/Debit Card')], default='Credit', max_length=255),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Accepted', 'Accepted'), ('Prepared', 'Prepared'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Active', max_length=255),
        ),
    ]
