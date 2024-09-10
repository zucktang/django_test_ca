from .models import User
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from rest_framework.authtoken.admin import TokenAdmin as BaseTokenAdmin
from rest_framework.authtoken.models import Token


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')
    


admin.site.register(User, UserAdmin)
