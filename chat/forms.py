import imp
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import User  
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import PasswordChangeForm


class Form(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'form-control'}),label='User')
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number', 'class': 'form-control', 'maxlength': '10'}),label='Mobile Number')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'form-control'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'ReEnter Password', 'class': 'form-control'}),label='Confirm Password')
    class Meta:
        model = User
        fields = ["username", "mobile", "password1", "password2"]


class Profile_Form(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'form-control text-white', 'readonly':'','style':'cursor: not-allowed;'}),label='Username')
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number', 'class': 'form-control text-white', 'maxlength': '10','readonly':'','style':'cursor: not-allowed;'}),label='Mobile Number')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'class': 'form-control text-white'}),label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'class': 'form-control text-white'}),label='Last Name', required=False)

    class Meta:
        model = Profile
        fields = ["username","mobile","first_name","last_name","profile_pic"]


class Reset_Password_Form(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Old Password', 'class': 'form-control text-white','type' : 'password' }),label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new Password', 'class': 'form-control text-white', 'type' : 'password'}), label='New Password',)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password', 'class': 'form-control text-white', 'type' : 'password'}),label='Confirm New Password')
    
    class Meta:
        model = User
        fields = ["old_password","new_password1","new_password2"]
    