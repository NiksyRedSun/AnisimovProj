# Generated by Django 4.2.1 on 2024-01-31 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_cart_item_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_num',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Номер телефона'),
        ),
    ]