# Generated by Django 5.0.3 on 2024-11-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0029_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='jRBeBEUOwv4lmBsPJfzPqhhlRLQWdGqq', editable=False, max_length=32, unique=True),
        ),
    ]