from django.shortcuts import render
from .models import UserProfile, CreateSession, Session, sessRatio
from profil import settings
from django.views.generic import TemplateView,View
import os
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from datetime import datetime
# Create your views here.

KEYS = []

class UserView(TemplateView):
    model = UserProfile
    template_name = 'user_view.html'

class BaseView(View):
    model = UserProfile
    template_name = 'base.html'
    def get(self, request, *args, **kwargs):
        button_name = 'Zaloguj'
        button_action = 'login/'
        form = 'login.html'
        url = os.path.join(settings.MEDIA_URL, 'anonymous.png')
        username = 'Anonymous'
        session = CreateSession(request)
        ##get session similar to current sess
        sessionSpace = Session.objects.all().order_by('date')
        if request.user.is_authenticated:
            username = request.user.username
            button_name = 'Wyloguj'
            button_action = 'logout/'
            form = 'empty.html'
            try:
                profile = UserProfile.objects.get(user=request.user)
                if profile != None:
                    url = profile.avatar.url
            except:
                pass
        return render(request, 'base.html', {'avatarurl':url, 'username':username, 'button_name':button_name, 'button_action':button_action, 'form':form, 'model':sessionSpace})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        usr = request.GET.get('username')
        pwd = request.GET.get('password')
        user = authenticate(request, username=usr, password=pwd)
        if user is not None:
            login(request, user)
        return redirect('/')
