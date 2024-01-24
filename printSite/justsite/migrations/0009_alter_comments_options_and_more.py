# Generated by Django 4.2.1 on 2024-01-23 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('justsite', '0008_alter_items_tags_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-time_create'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddIndex(
            model_name='comments',
            index=models.Index(fields=['-time_create'], name='justsite_co_time_cr_a21588_idx'),
        ),
    ]