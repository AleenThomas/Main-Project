# Generated by Django 4.2.4 on 2024-03-20 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0051_order_accepted_by_store_order_order_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('vehicle_type', models.CharField(max_length=20)),
                ('license_number', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('id_proof', models.ImageField(upload_to='id_proof/')),
                ('locality', models.CharField(max_length=255)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
