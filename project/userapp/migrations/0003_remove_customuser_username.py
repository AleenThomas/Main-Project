# Generated by Django 4.2.4 on 2023-09-14 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
