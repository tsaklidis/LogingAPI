# coding: utf-8
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

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

            total_valid_tokens = Token.objects.filter(
                user=user, invalid=False
            ).filter(
                Q(expiration__isnull=True) | Q(expiration__gt=timezone.now())
            ).count()
            if total_valid_tokens < settings.TOKENS_PER_USER:
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
            space_uuid = request.GET.get('space_uuid', False)
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

        # Collect all unique space UUIDs from the pack
        space_uuids = set()
        for item in request.data:
            space_uuid = item.get('space_uuid', False)
            if space_uuid:
                space_uuids.add(space_uuid)

        if not space_uuids:
            raise exceptions.PermissionDenied(
                detail="Provide correct data structure")

        # Batch-fetch all spaces in one query
        spaces = Space.objects.filter(uuid__in=space_uuids)
        if spaces.count() != len(space_uuids):
            raise exceptions.PermissionDenied(
                detail="One or more space UUIDs not found")

        # Verify ownership: all spaces must belong to houses owned by user
        owned_space_count = House.objects.filter(
            spaces__in=spaces, owner=request.user
        ).values('spaces').distinct().count()

        if owned_space_count != len(space_uuids):
            return False

        # Check pack size against sensor count
        first_space = spaces.first()
        house = get_object_or_404(House, spaces=first_space, owner=request.user)
        if len(request.data) > house.sensors_count:
            raise exceptions.PermissionDenied(
                detail="Data package to big, reduce measurement amount")

        return True


class IsAjax(permissions.BasePermission):
    message = "Only Ajax request allowed"

    def has_permission(self, request, view):
        if not request.is_ajax():
            return False
        return True