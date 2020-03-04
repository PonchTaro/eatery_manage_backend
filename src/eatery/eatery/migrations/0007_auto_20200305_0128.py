# Generated by Django 3.0.3 on 2020-03-05 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eatery', '0006_auto_20200305_0123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='orders',
            new_name='products',
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='注文数'),
        ),
    ]
