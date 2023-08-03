from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

class Admin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','mobile','password1','password2'),
        }),
    )

admin.site.register(get_user_model(),Admin)
admin.site.register(Profile)
admin.site.register(connectRequest)
admin.site.register(ConnectedNotification)
admin.site.register(ChatMessage)