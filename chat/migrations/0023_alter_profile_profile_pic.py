# Generated by Django 4.0 on 2023-08-03 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0022_alter_chatmessage_file_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
    ]
