from django.conf.urls import url
from django.contrib.auth import views as auth_views

from home_logs.accounts import views as accounts_v
from home_logs.accounts.forms import LoginAuthenticationForm

urlpatterns = [
    url('^home$', accounts_v.home, name='home'),

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
