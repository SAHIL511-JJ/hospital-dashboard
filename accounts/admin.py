# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra", {"fields": ("role", "profile_pic", "address_line1", "city", "state", "pincode")}),
    )

admin.site.register(User, UserAdmin)
