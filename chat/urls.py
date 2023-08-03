from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("register/",views.register, name="register"),
    path("login/",views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.user_profile, name="profile"),
    path("reset_password/",views.ResetPassword, name='reset_pass'),
    path("suggest/", views.suggest, name="suggest"),
    path("connect/",views.connect,name='connect'),
    path("notifications/", views.notifications, name="notifications"),
    path("connected/",views.connected,name='connected'),
    path("rejected/",views.rejected,name='rejected'),
    path('chat/<str:username>', views.chatuser, name='chat'),
    path('post_files/', views.FileUpload.as_view(), name="post_files"),
     path('download/<int:message_id>/', views.download_file, name='download_file'),
]