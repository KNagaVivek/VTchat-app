# Generated by Django 4.1.7 on 2023-07-28 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_connectrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectedNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(blank=True, null=True)),
                ('accepted', models.DateTimeField(auto_now_add=True, null=True)),
                ('saw', models.BooleanField(default=False)),
                ('dest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Destination_Notification', to=settings.AUTH_USER_MODEL)),
                ('sou', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Source_Notification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-accepted'],
            },
        ),
    ]