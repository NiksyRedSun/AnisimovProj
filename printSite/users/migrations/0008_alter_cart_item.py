# Generated by Django 4.2.1 on 2024-01-29 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('justsite', '0011_alter_comments_rating'),
        ('users', '0007_remove_cart_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='justsite.items'),
        ),
    ]