from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'authentication'

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'authentication/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'authentication/logout.html'}, name='logout'),
    url(r'^account/$', views.account, name='account'),
]
