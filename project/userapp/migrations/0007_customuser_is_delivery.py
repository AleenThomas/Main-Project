# Generated by Django 4.2.4 on 2024-03-20 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0006_customuser_hub_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_delivery',
            field=models.BooleanField(default=False),
        ),
    ]