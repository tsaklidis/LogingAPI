from django.conf.urls import url

from home_logs.api import views
from home_logs.custom_auth import views as auth_views


urlpatterns = [
    # House endpoints
    url(r'^house/all/$', views.HouseAllList.as_view(), name="all"),
    url(r'^house/my/$', views.HouseMyList.as_view(), name="my"),
    url(r'^house/(?P<uuid>\w+)/$', views.HouseSpecificList.as_view(),
        name="house_specific"),

    # Measurments
    url(r'^measurement/new/$', views.Measure.as_view(),
        name="measurement_new"),
    url(r'^measurement/pack/new/$', views.MeasurementPack.as_view(),
        name="measurement_pack"),
    url(r'^measurement/list/$', views.MeasureList.as_view(),
        name="measurement_list"),
    url(r'^measurement/list/last/$', views.MeasureListLast.as_view(),
        name="measurement_get_last"),

    # Public availale API data
    url(r'^open/measurement/list/$', views.OpenMeasureList.as_view(),
        name="open_measurement_list"),
    url(r'^open/measurement/list/last/$', views.OpenMeasureListLast.as_view(),
        name="open_measurement_get_last"),

    # Create a new persistent token, only for users with permission
    url(r'^token/persistent/new/$', auth_views.PersistentToken.as_view(),
        name='persistent_token'),
    # Create a new expiring token
    url(r'^token/expiring/new/$', auth_views.ExpiringToken.as_view(),
        name='expiring_token'),
    # Remind a token key
    url(r'^token/remember/$', auth_views.RememberToken.as_view(),
        name='remember_token'),
    # Invalidate a token
    url(r'^token/invalidate/$', auth_views.InvalidateToken.as_view(),
        name='invalidate_token'),
    url(r'^token/check/$', auth_views.CheckToken.as_view(),
        name='check_token'),
]
