# Generated by Django 4.2.11 on 2024-12-20 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0040_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='z2XK3La41Aj2wTMnxpqflxamt759D3MI', editable=False, max_length=32, unique=True),
        ),
    ]