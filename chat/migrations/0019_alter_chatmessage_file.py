# Generated by Django 4.0 on 2023-08-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_chatmessage_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static'),
        ),
    ]
