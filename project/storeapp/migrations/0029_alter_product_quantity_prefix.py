# Generated by Django 4.2.4 on 2023-10-04 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0028_remove_order_date_added_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_prefix',
            field=models.CharField(choices=[('gms', 'gms'), ('kg', 'kg')], default='gms', max_length=10, null=True),
        ),
    ]
