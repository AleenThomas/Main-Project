# Generated by Django 4.2.4 on 2024-02-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0039_remove_farm_visiting_hours_farm_visiting_hours_from_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farm_Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay_name', models.CharField(max_length=100)),
                ('rooms', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]
