# Generated by Django 4.2.4 on 2023-08-17 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0003_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
