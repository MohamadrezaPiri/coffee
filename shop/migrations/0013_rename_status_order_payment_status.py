# Generated by Django 4.2.3 on 2023-07-09 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='status',
            new_name='payment_status',
        ),
    ]
