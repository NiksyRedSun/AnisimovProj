# Generated by Django 4.2.1 on 2024-01-29 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_cart_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='count',
        ),
    ]