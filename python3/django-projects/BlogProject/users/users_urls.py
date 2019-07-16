from django.conf.urls import url
from .views import register, login

urlpatterns = [
    url(r'register/$', register, name='register-user'),
    url(r'login/$', login, name='login-user')
]