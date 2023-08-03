
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=10,unique=True, verbose_name="Mobile Number")
   
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["username"]
   

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles")
    username = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50, blank=True,null=True)
    last_name = models.CharField(max_length=50, blank=True,null=True)
    profile_pic = models.ImageField(upload_to="img", blank=True, null=True)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

class connectRequest(models.Model):
    source = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_sender')
    dest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_receiver')
    saw = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.source.username} sent {self.dest.username} a connection request"


class ConnectedNotification(models.Model):
    source = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="Source_Notification")
    dest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="Destination_Notification")
    desc = models.TextField(blank=True,null=True)
    accepted = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    saw = models.BooleanField(default=False)

    class Meta:
        ordering = ["-accepted"]

    def __str__(self) -> str:
        return f"{self.source.username} accepted your connection" 



class Message(models.Model):
    source = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    dest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username} ({self.timestamp})'



class ChatMessage(models.Model):
    source = models.CharField(max_length=100, default=None)
    msg = models.TextField(null=True, blank=True)
    thread = models.CharField(null=True, blank=True, max_length=50)
    file = models.FileField(upload_to='attachment/', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.msg