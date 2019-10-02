from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status

from home_logs.custom_auth.models import Token
from home_logs.custom_auth.permissions import ExceedMaxTokens, TokenOwner, PersistentTokens, AllowTokens

from home_logs.custom_auth.utils import update_token
from home_logs.utils import sanitize
from home_logs.utils.time_calculate import days_hence
from home_logs.utils.unique import get


class PersistentToken(ObtainAuthToken, ):
    '''
    Create persistent tokens
    '''

    permission_classes = (PersistentTokens, ExceedMaxTokens, AllowTokens,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        name = request.data.get('token_name', None)
        try:
            sanitize.alphanumeric(name)
        except sanitize.SanitizationException as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        if not name:
            errors = {"error": "Provide token_name"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            if not Token.objects.filter(user=user, name=name).exists():
                token = Token.objects.create(user=user, name=name)
                data = {
                    'token': token.key,
                    'token_name': name,
                    'expiration': 'Never'
                }
                return Response(data)
            else:
                data = {
                    'error': 'Token name exists'
                }
                return Response(data, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpiringToken(ObtainAuthToken, ):
    '''
    Create token that expires every 1 day
    Used for login in users from mobile and desktop clients
    '''

    permission_classes = (ExceedMaxTokens, AllowTokens, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        name = request.data.get('token_name', None)
        if not name:
            errors = {"error": "Provide token_name"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            sanitize.alphanumeric(name)
        except sanitize.SanitizationException as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token_exists = Token.objects.filter(user=user, name=name).exists()

            if not token_exists:
                # Create new token
                token = Token.objects.create(user=user, name=name,
                                             expiration=days_hence())
                data = {
                    'token': token.key,
                    'expiration': token.expiration.strftime('%Y-%m-%d %H:%M:%S')
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                # Token exists, check if has expired
                token = Token.objects.get(user=user, name=name)

                if token.expired or token.invalid:
                    # Update expired token
                    token = update_token(token)

                    data = {
                        'info': 'Token updated',
                        'token': token.key,
                        'expiration': token.expiration.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data = {
                        'error': 'Valid token with same name exists',
                    }
                    return Response(data, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RememberToken(ObtainAuthToken, ):
    '''
    Remind a specific token based on name
    '''

    permission_classes = (TokenOwner, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            name = request.data.get('token_name', None)
            if not name:
                errors = {"error": "Provide token_name"}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            try:
                sanitize.alphanumeric(name)
            except sanitize.SanitizationException as e:
                return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

            token = Token.objects.get(user=user, name=name)
            if token.expiration:
                expiration = token.expiration.strftime('%Y-%m-%d %H:%M:%S')
            else:
                expiration = None
            data = {
                'token': token.key,
                'expiration': expiration,
                'expired': token.expired
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvalidateToken(ObtainAuthToken, ):
    '''
    Invalidate a specific token based on name and key
    '''

    permission_classes = (TokenOwner, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            name = request.data.get('token_name', None)
            key = request.data.get('key', None)
            if not (name and key):
                errors = {"error": "Provide token_name and key"}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            try:
                sanitize.alphanumeric(name)
            except sanitize.SanitizationException as e:
                return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

            # token = Token.objects.get(user=user, name=name, key=key)
            token = get_object_or_404(Token, user=user, name=name, key=key)
            token.invalid = True
            token.save()
            data = {
                'info': 'Token invalidated',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckToken(ObtainAuthToken):
    '''
    Check if a provided token is valid
    '''

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            key = request.data.get('key', None)
            if not key:
                errors = {"error": "Provide token_name and key"}
                return Response(errors, status=status.HTTP_400_BAD_REQUES)

            valid = Token.objects.filter(user=user, key=key, invalid=False,
                                        expiration__gt=timezone.now()).exists()

            return Response({"valid": valid}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
