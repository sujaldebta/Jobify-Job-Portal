from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('is_seeker', 'is_recruiter')}),
    )

admin.site.register(User, CustomUserAdmin)
