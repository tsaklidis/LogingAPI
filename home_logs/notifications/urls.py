from django.conf.urls import url

from home_logs.notifications import views


urlpatterns = [
    url('', views.alerts, name='alerts_index'),

]
