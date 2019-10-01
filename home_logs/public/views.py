from django.conf import settings
from django.db.models import Avg, Max, Min
from django.utils import timezone
from pytz import timezone as timezone_pytz

from django.shortcuts import render

from home_logs.logs.models import Measurement


def public(request):
    # This is public landing page
    # Measurements are not filtered by user!
    custom_date = request.GET.get('date', False)

    date = timezone.localtime(timezone.now())
    hour_from = request.GET.get('hour_from', date.hour)
    hour_to = request.GET.get('hour_to', date.hour + 1)

    if hour_from or hour_to:
        try:
            hour_to = int(hour_to)
            hour_from = int(hour_from)
        except Exception as e:
            hour_from = 0
            hour_to = 23

    if custom_date:
        try:
            date = timezone.datetime.strptime(custom_date, '%d-%b-%Y')
            date = date.replace(tzinfo=timezone_pytz(settings.TIME_ZONE))
        except Exception as e:
            print e
            date = timezone.localtime(timezone.now())

    ms = Measurement.objects.filter(created_on__date__day=date.day,
                                    created_on__date__month=date.month,
                                    created_on__hour__range=(
                                        hour_from, hour_to),
                                    # created_on__minute=15,
                                    )

    dht22_h = ms.filter(sensor__name='DHT22', sensor__kind__name='humidity')
    dht22_t = ms.filter(sensor__name='DHT22', sensor__kind__name='temperature')
    ds18b20 = ms.filter(sensor__name='DS18B20')

    avg = ds18b20.aggregate(Avg('value'))
    ds_min = ds18b20.aggregate(Min('value'))
    ds_max = ds18b20.aggregate(Max('value'))

    data = {
        'dht22_h': dht22_h,
        'dht22_t': dht22_t,
        'ds18b20': ds18b20,
        'avg': round(avg['value__avg'], 2),
        'min': round(ds_min['value__min'], 2),
        'max': round(ds_max['value__max'], 2),
        'date': date,
        'hour_from': hour_from,
        'hour_to': hour_to,
    }

    return render(request, 'public/public.html', data)


def no_rights(request):
    data = {}
    return render(request, 'public/norigths.html', data)
