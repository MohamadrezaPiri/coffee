# Generated by Django 4.2.3 on 2023-07-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order_item_order_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderid',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
