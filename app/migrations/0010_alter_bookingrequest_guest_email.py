# Generated by Django 4.2.22 on 2025-06-18 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_bookingrequest_guest_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingrequest',
            name='guest_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
