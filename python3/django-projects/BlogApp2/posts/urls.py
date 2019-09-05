from django.urls import path, re_path
from .views import post_list, post_detail, post_create, post_update, post_delete

urlpatterns = [
    path('', post_list, name='post-home'),
    re_path('create/', post_create, name='post-create'),
    re_path('^detail/(?P<pid>\d+)/$', post_detail, name='post-detail'),
    re_path('^update/(?P<pid>\d+)/$', post_update, name='post-update'),
    re_path('^delete/(?P<pid>\d+)/$', post_delete, name='post-delete'),

]
