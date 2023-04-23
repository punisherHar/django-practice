from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import UserInfo
from .forms import UserInfoForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# Create your views here.

def base(request):
    return render(request,'base.html')

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            users = UserInfo(user=user)
            users.save()
            return redirect('index')
    else:
        form = UserInfoForm()
    return render(request, 'registration/register.html',{'form':form})
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
    
            else:
                return HttpResponse("account not active")
        else:
            error_msg = "Invalid username or password."
            return HttpResponse(error_msg)
    else:
        return render(request,'login.html')
    


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    success_url = '/reset_password_sent/'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = '/reset_password_complete/'