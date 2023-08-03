
from ast import For
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout,get_user_model
from django.contrib.auth.decorators import login_required
import json
from django.views import View
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
# Create your views here.

def get_friends_data(user):
    cur_user = Profile.objects.get(user=user)
    friends = cur_user.friends.all()
    friends_profile_pics = []
    for friend in friends:
        friend_profile = Profile.objects.get(user=friend)
        if friend_profile.profile_pic:
            friends_profile_pics.append(friend_profile.profile_pic.url)
        else:
            friends_profile_pics.append('/static/img/user.png')
    friends_data = zip(friends, friends_profile_pics)
    return friends_data


@login_required(login_url="login")
def index(request):
    friends_data = get_friends_data(request.user)
    cur_user = Profile.objects.get(user=request.user)
    req = connectRequest.objects.filter(dest=request.user)
    context = {
        'friends_data': friends_data,
        'cur_user' : cur_user,
        'notify' : req,
    }
    return render(request,'index.html', context)

def chatuser(request,username):
    friends_data = get_friends_data(request.user)
    cur_user = Profile.objects.get(user=request.user)
    obj = Profile.objects.get(username=username) 
    req = connectRequest.objects.filter(dest=request.user)
    if request.user.id > obj.id:
        thread = f"chat_{request.user.id}-{obj.id}"
    else:
        thread = f"chat_{obj.id}-{request.user.id}"
    msg_obj = ChatMessage.objects.filter(thread = thread)
    context = {
        'friends_data': friends_data,
        'user_obj' : obj,
        'msg_obj' : msg_obj,
        'cur_user' : cur_user,
        'notify' : req,
    }
    return render(request,'chat.html',context)

class FileUpload(View):
    def post(self, request):
        files = request.FILES.get('files')
        message = request.POST.get('message')
        username = request.POST.get('username')
        print(files,message,username)
        try:
            chat_message = ChatMessage.objects.filter(source=username, msg=message).last()
            if chat_message is not None:
                chat_message.file = files
                chat_message.save()
            else:
                return HttpResponse("ChatMessage does not exist.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

        return HttpResponse("File Successfully added!")
    

def download_file(request, message_id):
    chat_message = get_object_or_404(ChatMessage, id=message_id)
    file_path = chat_message.file.path  
    response = FileResponse(open(file_path, 'rb'))
    return response


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    user = Form()
    if request.method == 'POST':
        user = Form(request.POST)
        if user.is_valid():
            user.save()

            mobile = request.POST['mobile']
            pas = request.POST['password1']
            user_login = authenticate(request, mobile=mobile,password=pas)
            if user_login is not None:
                auth_login(request,user_login)
                return redirect('index')
    return render(request, 'register.html', {'Form':user})


def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']

        user = authenticate(request, mobile = mobile, password = password)

        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Mobile Number/password')
            return redirect('login') 
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url="login")
def user_profile(request):
    friends_data = get_friends_data(request.user)
    user = request.user
    profile = Profile.objects.get(user=user)
    form = Profile_Form(instance=profile)
    req = connectRequest.objects.filter(dest=request.user)
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'friends_data': friends_data,
        'form':form,
        'cur_user' : profile,
        'notify' : req,
    }
    return render(request, 'profile.html', context)

def ResetPassword(request):
    if request.method == 'POST':
        reset_form = Reset_Password_Form(request.user, request.POST)
        if reset_form.is_valid():
            reset_form.save()
            return redirect('profile')
    else:
        reset_form = Reset_Password_Form(request.user)
    friends_data = get_friends_data(request.user)
    profile = Profile.objects.get(user=request.user)
    req = connectRequest.objects.filter(dest=request.user)
    context = {
        'friends_data': friends_data,
        'cur_user' : profile,
        'notify' : req,
        'reset_form' : reset_form,
    }
    return render(request, 'reset_pass.html', context=context)

@login_required(login_url="login")
def suggest(request):
    friends_data = get_friends_data(request.user)
    all_profiles = get_user_model()
    user = request.user
    profile = Profile.objects.get(user=user)
    friends = profile.friends.all()
    sugg = all_profiles.objects.exclude(profile__friends__in = friends).exclude(profiles=profile)
    cont_reqst = connectRequest.objects.filter(dest__in = sugg, source = request.user)
    req = connectRequest.objects.filter(dest=user)
    context = {
        'friends_data': friends_data,
        'friends':sugg,
        'users':cont_reqst,
        'cur_user' : profile,
        'notify' : req,
    }
    return render(request, 'suggestions.html',context)

def connect(request):
    content = json.loads(request.body)
    profile = get_user_model()
    dest = profile.objects.get(id = content)
    req = connectRequest.objects.create(source=request.user,dest=dest)
    return JsonResponse("sending....", safe=False)

@login_required(login_url="login")
def notifications(request):
    friends_data = get_friends_data(request.user)
    user = request.user
    cur_user = Profile.objects.get(user=user)
    req = connectRequest.objects.filter(dest=user)
    context = {
        'friends_data' : friends_data,
        'notify' : req,
        'cur_user' : cur_user
    }
    return render(request, 'notification.html',context)


def connected(request):
    data = json.loads(request.body)
    user = get_user_model()
    users = user.objects.get(id = data)
    profile = Profile.objects.get(user_id = request.user.id)
    profile2 = Profile.objects.get(user_id = data)
    req = connectRequest.objects.get(source=users,dest=request.user)
    
    msg = None
    if profile:
        if profile.friends.filter(id=data).exists():
            profile.friends.remove(users)
            msg="no"
        else:
            profile.friends.add(users)
            req.delete()
            notify = ConnectedNotification.objects.create(source=request.user, dest=users, desc=f"{request.user.username} accepted your connection")
            msg="yes"
    if profile2:
        if profile2.friends.filter(id=request.user.id).exists():
            profile2.friends.remove(request.user)
        else:
            profile2.friends.add(request.user)

    return JsonResponse(msg,safe=False)


def rejected(request):
    data = json.loads(request.body)
    user = get_user_model()
    users = user.objects.get(id = data)
    profile = Profile.objects.get(user_id = request.user.id)
    req = connectRequest.objects.get(source=users,dest=request.user)
    try:
        req = connectRequest.objects.get(source=users, dest=request.user)
        req.delete()
    except ObjectDoesNotExist:
        return JsonResponse("Connection request not found.", status=404)

    return JsonResponse("Rejected", safe=False)