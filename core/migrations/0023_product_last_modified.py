# Generated by Django 4.2.11 on 2024-10-05 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_product_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
