from django.conf.urls import include, url
from django.contrib import admin
import family.urls as family_urls


urlpatterns = [
    # Examples:
    # url(r'^$', 'tryformsets18.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^family/', include(family_urls)),
]
