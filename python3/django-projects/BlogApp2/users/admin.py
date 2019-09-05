from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User


# Register your models here.

class CustomAdmin(UserAdmin):
    fieldsets = ((None, {"fields": ("first_name", "last_name", "username", "email", "password",
                                    "description")}),)
    add_fieldsets = ((None, {"fields": ("first_name", "last_name", "username", "email", "password",
                                        "description")}),)
    list_display = ["username", "first_name", "last_name", "email"]


admin.site.register(User, CustomAdmin)
