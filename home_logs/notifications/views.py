from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test

from home_logs.notifications.models import Alert


def alerts_allowed(user):
    return user.allow_alerts


@user_passes_test(alerts_allowed, login_url='public:no_rights')
@login_required
def alerts(request):
    alerts = Alert.objects.filter(creator=request.user)
    data = {
        'alerts': alerts
    }
    return render(request, 'private/alerts.html', data)