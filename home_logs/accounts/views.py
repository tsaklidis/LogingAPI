from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from home_logs.property.models import House
from home_logs.custom_auth.models import Token


def allowed(user):
    CustomUser = get_user_model()
    return CustomUser.objects.filter(id=user.id, allow_panel=True)


@user_passes_test(allowed, login_url='user:auth_login')
@login_required
def home(request):
    houses = House.objects.filter(owner=request.user)
    token = Token.objects.filter(user=request.user).last()
    data = {
        "houses": houses,
        "token": token.key,
    }
    return render(request, 'private/home.html', data)
