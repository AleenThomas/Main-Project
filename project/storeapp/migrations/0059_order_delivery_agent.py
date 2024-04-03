# Generated by Django 4.2.4 on 2024-04-01 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0058_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_agent',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='storeapp.deliveryagent'),
        ),
    ]