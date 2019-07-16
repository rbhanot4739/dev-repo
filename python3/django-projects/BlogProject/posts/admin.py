from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "create_time", "update_time"]
    search_fields = ["title"]
    list_filter = ["title"]
    ordering = ["-update_time"]


admin.site.register(Post, PostAdmin)
