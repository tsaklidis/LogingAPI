from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404

from home_logs.property.models import House, Space
from home_logs.custom_auth.models import Token


def allowed(user):
    CustomUser = get_user_model()
    return CustomUser.objects.filter(id=user.id, allow_panel=True)


@user_passes_test(allowed, login_url='user:auth_login')
@login_required
def home(request):
    houses = House.objects.filter(owner=request.user)
    data = {
        "houses": houses,
    }
    return render(request, 'private/home.html', data)


@user_passes_test(allowed, login_url='user:auth_login')
@login_required
def house(request, uuid=None):
    house = House.objects.get(owner=request.user, uuid=uuid)
    data = {
        "house": house,
    }
    return render(request, 'private/house_specific.html', data)


@user_passes_test(allowed, login_url='user:auth_login')
@login_required
def spaces(request):
    spaces = Space.objects.filter(owner=request.user)
    data = {
        "spaces": spaces,

    }
    return render(request, 'private/spaces.html', data)


@user_passes_test(allowed, login_url='user:auth_login')
@login_required
def space(request, uuid=None):
    space = get_object_or_404(Space, uuid=uuid, owner=request.user)

    data = {
        "space": space,
    }
    return render(request, 'private/space.html', data)
