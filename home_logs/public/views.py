from django.conf import settings
from django.core.cache import cache
from django.db.models import Avg, Max, Min
from django.utils import timezone
from pytz import timezone as timezone_pytz

from django.shortcuts import render

from home_logs.logs.models import Measurement


def public(request, lang=None, *args, **kwargs):
    # This is public landing page
    # Measurements are not filtered by user!

    # Cache the count for 5 minutes to avoid expensive COUNT(*) on every load
    cache_key = 'public_total_ms'
    total_ms = cache.get(cache_key)
    if total_ms is None:
        total_ms = Measurement.objects.filter(
            space__uuid=settings.PUBLIC_SPACE
        ).count()
        cache.set(cache_key, total_ms, 300)  # 5 minutes

    data = {
       'total_ms': total_ms
    }
    if lang == 'en':
        template = 'public/public.html'
    else:
        template = 'public/public_el_new.html'

    return render(request, template, data)


def no_rights(request):
    data = {}
    return render(request, 'public/norigths.html', data)
