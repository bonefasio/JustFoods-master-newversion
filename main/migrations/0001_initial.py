# Generated by Django 3.1.7 on 2021-06-09 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer_order_total', models.FloatField(blank=True, default=12.3, null=True)),
                ('employee_id', models.CharField(default=12.3, max_length=50)),
                ('registered_payroll', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomMeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_meal_name', models.CharField(max_length=150)),
                ('patron_first_name', models.CharField(max_length=150)),
                ('patron_last_name', models.CharField(max_length=150)),
                ('patron_email_address', models.CharField(max_length=50)),
                ('patron_phone_contact', models.CharField(max_length=50)),
                ('meal_request_date', models.DateTimeField(null=True)),
                ('meal_reqest_time', models.TimeField(blank=True, null=True)),
                ('order_quantity', models.IntegerField(default=0)),
                ('custom_meal_receipe', models.CharField(max_length=100)),
                ('custom_meal_ingredients', models.CharField(max_length=100)),
                ('request_order_status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Accepted', 'Accepted'), ('Prepared', 'Prepared'), ('Pending Delivery', 'Pending Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Pending', max_length=255)),
                ('custom_meal_price', models.FloatField(default=False)),
            ],
            options={
                'verbose_name': 'Custom Meal Order',
                'verbose_name_plural': 'Custom Meal Orders',
            },
        ),
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
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('price', models.FloatField()),
                ('instructions', models.CharField(blank=True, choices=[('Pickup', 'Pickup'), ('Delivery Available', 'Delivery Available'), ('Both Available [Pickup & Delivery Available]', 'Both Available [Pickup & Delivery Available]')], max_length=250)),
                ('image', models.ImageField(default='default.png', upload_to='images/')),
                ('labels', models.CharField(blank=True, choices=[('BestSeller', 'BestSeller'), ('New', 'New'), ('Spicy🔥', 'Spicy🔥'), ('Veggies', 'Veggies')], max_length=25)),
                ('label_colour', models.CharField(blank=True, choices=[('danger', 'danger'), ('success', 'success'), ('primary', 'primary'), ('info', 'info')], max_length=15)),
                ('slug', models.SlugField(default='slug', max_length=255)),
                ('quantity_available', models.IntegerField(default=1)),
                ('subcription_avail', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Food Item',
                'verbose_name_plural': 'Food Items',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='USP', max_length=50)),
                ('address', models.CharField(blank=True, max_length=80)),
                ('category', models.CharField(choices=[('OnSite', 'OnSite'), ('OffSite', 'OffSite'), ('Direct Pickup', 'Direct Pickup')], default='OnSite', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rslug', models.SlugField(max_length=255)),
                ('review', models.TextField()),
                ('posted_on', models.DateField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_balance', models.FloatField(blank=True, default=134.34, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('registered', models.BooleanField(default=False)),
                ('employee_id', models.CharField(max_length=200, null=True)),
                ('birth_date', models.DateTimeField(null=True)),
                ('customer_acc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.customer')),
            ],
            options={
                'verbose_name': 'Payroll',
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('ordered_date', models.DateField()),
                ('payment_method', models.CharField(choices=[('Payroll', 'Payroll'), ('Credit/Debit Card', 'Credit/Debit Card')], default='Credit', max_length=255)),
                ('status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Accepted', 'Accepted'), ('Prepared', 'Prepared'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Active', max_length=255)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_mode', models.CharField(choices=[('Delivered (On Site Campus)', 'Delivered (On Site Campus)'), ('Delivered (Off Site Campus) *limited sites', 'Delivered (Off Site Campus) *limited sites'), ('PickUp', 'PickUp')], max_length=255)),
                ('isPaid', models.BooleanField(default=False)),
                ('paidAt', models.DateTimeField(blank=True, null=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('subscription_order', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.customer')),
                ('delivery_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.location')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.item')),
            ],
            options={
                'verbose_name': 'Food Order Item',
                'verbose_name_plural': 'Food Order Items',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Display', 'Display'), ('Hide', 'Hide')], max_length=25)),
                ('items', models.ManyToManyField(to='main.Item')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='MealSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_available', multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=255)),
                ('time_ordered', models.TimeField(null=True)),
                ('delivery_mode', models.CharField(choices=[('Delivered (On Site Campus)', 'Delivered (On Site Campus)'), ('Delivered (Off Site Campus) *limited sites', 'Delivered (Off Site Campus) *limited sites'), ('PickUp', 'PickUp')], max_length=255)),
                ('payment_method', models.CharField(choices=[('Payroll', 'Payroll'), ('Credit', 'Credit')], default='Credit', max_length=255)),
                ('subscription_status', models.BooleanField(default=False)),
                ('number_days', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Accepted', 'Accepted'), ('Prepared', 'Prepared'), ('Pending Delivery', 'Pending Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Active', max_length=255)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('delivery_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.location')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.item')),
            ],
            options={
                'verbose_name': 'Meal Subscription',
                'verbose_name_plural': 'Meal Subscriptions',
            },
        ),
    ]
