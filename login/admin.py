from django.contrib import admin
from .models import UserProfile, Session
# Register your models here.
admin.site.register(UserProfile)

admin.site.register(Session)