# Generated by Django 4.2.11 on 2024-10-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0011_customuser_remove_profile_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
