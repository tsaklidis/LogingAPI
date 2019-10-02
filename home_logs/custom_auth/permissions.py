# coding: utf-8
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions, exceptions

from home_logs.property.models import House, Space
from home_logs.custom_auth.models import Token


class AllowTokens(permissions.BasePermission):
    message = 'You are not allowed to create tokens'

    def has_permission(self, request, view):
        User = get_user_model()
        username = request.data.get('username', False)
        user = get_object_or_404(User, username=username)
        if not user.allow_tokens:
            raise exceptions.PermissionDenied(detail=self.message)
        return user.allow_tokens


class PersistentTokens(permissions.BasePermission):
    message = 'Not enough permissions for creating persistent token'

    def has_permission(self, request, view):
        User = get_user_model()
        username = request.data.get('username', False)
        user = get_object_or_404(User, username=username)
        if not user.persistent_tokens:
            raise exceptions.PermissionDenied(detail=self.message)
        return True


class ExceedMaxTokens(permissions.BasePermission):
    message = 'Valid Token limit ({}) reached.'.format(
        settings.TOKENS_PER_USER)

    def has_permission(self, request, view):
        username = request.data.get("username", False)
        if username:

            User = get_user_model()
            user = get_object_or_404(User, username=username)
            if user.unlimited_tokens:
                return True

            total_tokens = [tok for tok in Token.objects.filter(
                user__username=username) if not tok.expired]
            if len(total_tokens) < settings.TOKENS_PER_USER:
                return True
            # Normaly this is not needed.
            # some permissions mess probably, still searching...
            raise exceptions.PermissionDenied(detail=self.message)
        else:
            return False


class TokenOwner(permissions.BasePermission):
    message = "Token not found"

    def has_permission(self, request, view):
        username = request.data.get("username", False)
        token_name = request.data.get("token_name", False)

        if username and token_name:
            if Token.objects.filter(user__username=username, name=token_name).exists():
                return True
            raise exceptions.PermissionDenied(detail=self.message)
        else:
            return False


class IsHouseOwner(permissions.BasePermission):
    message = "House not found or not owned"

    def has_permission(self, request, view):
        uuid = view.kwargs.get('uuid', False)
        return House.objects.filter(uuid=uuid, owner=request.user).exists()


class IsSpaceOwner(permissions.BasePermission):
    message = "Space not found or not owned"

    def has_permission(self, request, view):
        try:
            space_uuid = request.data.get('space_uuid', False)
            space = get_object_or_404(Space, uuid=space_uuid)
        except AttributeError:
            raise exceptions.PermissionDenied(
                detail="Provide correct data structure")

        return House.objects.filter(spaces=space, owner=request.user).exists()


class IsSpaceOwnerPack(permissions.BasePermission):
    message = "Space not found or not owned"

    def has_permission(self, request, view):
        if not isinstance(request.data, list):
            raise exceptions.PermissionDenied(detail="Provide data in list []")
        # request.data is list:
        # [
        #     {"space_uuid":"c75","sensor_uuid":"3c", "value":25},
        #     {"space_uuid":"c75","sensor_uuid":"3c", "value":26},
        # ]
        # Find the count of sensors in house
        # Prevent big pack save to db
        space_uuid = request.data[0].get('space_uuid', False)
        space = get_object_or_404(Space, uuid=space_uuid)
        house = get_object_or_404(House, spaces=space, owner=request.user)
        if len(request.data) > house.sensors_count:
            raise exceptions.PermissionDenied(
                detail="Data package to big, reduce measurement amount")

        spaces = []
        for item in request.data:
            space_uuid = item.get('space_uuid', False)
            space = get_object_or_404(Space, uuid=space_uuid)
            if not House.objects.filter(spaces=space, owner=request.user).exists():
                return False
            else:
                spaces.append(space)
        return True
