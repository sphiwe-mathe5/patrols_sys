# Generated by Django 5.0.3 on 2024-08-19 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0008_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total_posts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
