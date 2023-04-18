from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User
from django.contrib import admin
from .models import Staff, LoginCredential
class UserAdmin(DefaultUserAdmin):
    # You can customize the admin interface here if needed.
    # By default, it will inherit the settings from Django's UserAdmin class.
    pass


admin.site.register(LoginCredential)