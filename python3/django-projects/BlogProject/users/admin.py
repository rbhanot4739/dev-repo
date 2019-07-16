from django.contrib import admin
from .models import CustomUser


# Register your models here.

class CustomAdmin(admin.ModelAdmin):
    # fields = ["first_name", "last_name", "username", "email", "password", "description"]
    list_display = ["first_name", "last_name", "email"]


admin.site.register(CustomUser, CustomAdmin)
