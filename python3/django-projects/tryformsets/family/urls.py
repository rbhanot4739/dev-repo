from django.urls import re_path, path
from .views import create_family_member, add_child

urlpatterns = [
    re_path('^add_edit/(?P<pk>\d+)/$', create_family_member, name='update-member'),
    path('add_child/', add_child, name='add-child'),

]