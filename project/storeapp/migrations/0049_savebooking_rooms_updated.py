# Generated by Django 4.2.4 on 2024-03-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0048_savebooking_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='savebooking',
            name='rooms_updated',
            field=models.BooleanField(default=False),
        ),
    ]
