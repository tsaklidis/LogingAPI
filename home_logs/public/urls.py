from django.conf.urls import url

from home_logs.public import views


urlpatterns = [
    url('^$', views.public, name='public'),
    url('^norights/$', views.no_rights, name='no_rights'),

]
