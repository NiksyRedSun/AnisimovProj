# Generated by Django 4.2.1 on 2024-01-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justsite', '0012_order_orderitem_order_justsite_or_time_cr_8bbbfb_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='justsite.tagitem', verbose_name='Теги'),
        ),
    ]