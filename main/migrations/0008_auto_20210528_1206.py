# Generated by Django 3.1.7 on 2021-05-28 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210523_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=150)),
                ('item_purchase_date', models.DateTimeField(blank=True, null=True)),
                ('item_purchase_expirydate', models.DateTimeField(blank=True, null=True)),
                ('item_quantity_available', models.IntegerField(default=0)),
                ('item_purchase_price', models.FloatField(default=False)),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.AddField(
            model_name='mealsubscription',
            name='status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Accepted', 'Accepted'), ('Prepared', 'Prepared'), ('Pending Delivery', 'Pending Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Active', max_length=255),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Accepted', 'Accepted'), ('Prepared', 'Prepared'), ('Pending Delivery', 'Pending Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Active', max_length=255),
        ),
    ]
