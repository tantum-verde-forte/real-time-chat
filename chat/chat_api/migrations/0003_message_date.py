# Generated by Django 4.1.7 on 2023-02-25 16:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat_api', '0002_alter_message_text_alter_message_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
