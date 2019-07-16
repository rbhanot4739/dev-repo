from django.conf.urls import url

from .views import post_create, post_delete, post_detail, post_list, post_update

urlpatterns = [
    url(r'^$', post_list, name="post-home"),
    url(r'^detail/(?P<pid>\d+)$', post_detail, name="post-detail"),
    url(r'^create/$', post_create, name='post-create'),
    url(r'^update/(?P<pid>\d+)$', post_update, name='post-update'),
    url(r'^delete/(?P<pid>\d+)$', post_delete, name='post-delete'),
]
