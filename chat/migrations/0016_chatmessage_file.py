# Generated by Django 4.0 on 2023-08-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_remove_chatmessage_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='attachments'),
        ),
    ]
