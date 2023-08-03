# Generated by Django 4.0 on 2023-08-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_alter_chatmessage_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='attachment/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]
