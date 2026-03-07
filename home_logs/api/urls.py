from django.urls import re_path

from home_logs.api import views
from home_logs.custom_auth import views as auth_views


urlpatterns = [
    # House endpoints
    re_path(r'^house/all/$', views.HouseAllList.as_view(), name="all"),
    re_path(r'^house/my/$', views.HouseMyList.as_view(), name="my"),
    re_path(r'^house/(?P<uuid>\w+)/$', views.HouseSpecificList.as_view(),
        name="house_specific"),

    # Measurments
    re_path(r'^measurement/new/$', views.Measure.as_view(),
        name="measurement_new"),
    re_path(r'^measurement/pack/new/$', views.MeasurementPack.as_view(),
        name="measurement_pack"),
    re_path(r'^measurement/list/$', views.MeasureList.as_view(),
        name="measurement_list"),
    re_path(r'^measurement/list/last/$', views.MeasureListLast.as_view(),
        name="measurement_get_last"),

    # Public availale API data
    re_path(r'^open/measurement/list/$', views.OpenMeasureList.as_view(),
        name="open_measurement_list"),
    re_path(r'^open/measurement/list/last/$', views.OpenMeasureListLast.as_view(),
        name="open_measurement_get_last"),

    # Create a new persistent token, only for users with permission
    re_path(r'^token/persistent/new/$', auth_views.PersistentToken.as_view(),
        name='persistent_token'),
    # Create a new expiring token
    re_path(r'^token/expiring/new/$', auth_views.ExpiringToken.as_view(),
        name='expiring_token'),
    # Remind a token key
    re_path(r'^token/remember/$', auth_views.RememberToken.as_view(),
        name='remember_token'),
    # Invalidate a token
    re_path(r'^token/invalidate/$', auth_views.InvalidateToken.as_view(),
        name='invalidate_token'),
    re_path(r'^token/check/$', auth_views.CheckToken.as_view(),
        name='check_token'),
]
