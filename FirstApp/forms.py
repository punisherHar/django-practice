from django import forms
from django.contrib.auth.models import User
from .models import UserInfo
#create forms

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('username','password','email')