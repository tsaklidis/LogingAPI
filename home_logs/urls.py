from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url('panel/', admin.site.urls),
    url('^', include('home_logs.public.urls', 'public')),
    url('user/', include('home_logs.accounts.urls', 'user')),
    url('api/', include('home_logs.api.urls')),
]
