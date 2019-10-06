from django.conf.urls import url
from django.contrib.auth import views as auth_views

from home_logs.accounts import views as accounts_v
from home_logs.accounts.forms import LoginAuthenticationForm

urlpatterns = [
    url('^home$', accounts_v.home, name='home'),
    url('^house/(?P<uuid>\w+)/$', accounts_v.house, name='house'),

    url('^spaces/$', accounts_v.spaces, name='spaces'),

    url('^space/(?P<uuid>\w+)/$', accounts_v.space, name='space'),


    # Private area "/user" is difined at main urls.py
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'public/login.html',
         'authentication_form': LoginAuthenticationForm},
        name='auth_login'),

    url(r'^logout/$',
        auth_views.logout, {'template_name': 'public/logout.html'},
        name='auth_logout'),
]
