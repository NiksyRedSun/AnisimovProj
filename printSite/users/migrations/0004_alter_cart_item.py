# Generated by Django 4.2.1 on 2024-01-21 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('justsite', '0004_alter_items_cat_alter_items_tags'),
        ('users', '0003_alter_cart_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='justsite.items'),
        ),
    ]
