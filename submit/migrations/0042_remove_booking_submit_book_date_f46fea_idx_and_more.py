# Generated by Django 4.2.11 on 2024-12-20 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0041_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='booking',
            name='submit_book_date_f46fea_idx',
        ),
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='gjuDafFKvRpUZfBc3Y9PCf0ELp4FNXy8', editable=False, max_length=32, unique=True),
        ),
    ]