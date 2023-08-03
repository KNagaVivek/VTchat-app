from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def profile_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username, mobile = instance.mobile)




@receiver(post_save, sender=Profile)
def send_onlineStatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.username
        user_status = instance.status

        data = {
            'username':user,
            'status':user_status
        }
        async_to_sync(channel_layer.group_send)(
            'user', {
                'type':'send_onlineStatus',
                'value':json.dumps(data)
            }
        )
