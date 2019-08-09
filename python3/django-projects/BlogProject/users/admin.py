from django.contrib import admin
from .models import User


# Register your models here.

class CustomAdmin(admin.ModelAdmin):
    fields = ["first_name", "last_name", "username", "email", "password", "description"]
    list_display = ["first_name", "last_name", "email"]


admin.site.register(User, CustomAdmin)
