from django.conf.urls import include, url
from django.contrib import admin
import family.urls as family_urls
from .views import create_family_member, add_child


urlpatterns = [
    # Examples:
    # url(r'^$', 'tryformsets18.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^add_edit/(?P<pk>\d+)/$', create_family_member, name='update-member'),
    url(r'^add_child/$', add_child, name='add-child'),
]
