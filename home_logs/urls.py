from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url('^', include('home_logs.public.urls', 'public')),
    url('panel/', admin.site.urls),
    url('user/', include('home_logs.accounts.urls', 'user')),
    url('api/', include('home_logs.api.urls')),
]
