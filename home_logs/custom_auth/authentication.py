from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from home_logs.custom_auth.models import Token


class ExpiringToken(TokenAuthentication):
    '''
    Expiring token every 24hrs requiring to supply valid username
    and password for new one to be created.
    '''

    def authenticate_credentials(self, key, request=None):

        try:
            token = Token.objects.select_related('user').get(
                                                        key=key, invalid=False)
        except Token.DoesNotExist:
            raise AuthenticationFailed({'error': 'Invalid or Expired Token'})

        if not token.user.is_active:
            raise AuthenticationFailed({'error': 'Invalid user'})

        # TODO:
        # Add Invalidation after not using
        if token.expired:
            data = {
                'expiration_date': token.expiration,
                'error': 'Token has expired or is invalid',
            }
            raise AuthenticationFailed(data)
        return token.user, token
