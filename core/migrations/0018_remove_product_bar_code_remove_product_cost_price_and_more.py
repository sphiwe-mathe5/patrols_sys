# Generated by Django 4.2.11 on 2024-09-29 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_product_name_alter_product_bar_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bar_code',
        ),
        migrations.RemoveField(
            model_name='product',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='selling_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(default=12345, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=0, max_length=200),
        ),
    ]