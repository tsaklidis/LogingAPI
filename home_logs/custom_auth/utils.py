from home_logs.custom_auth.models import Token
from home_logs.utils.time_calculate import days_hence
from home_logs.utils.unique import get

def update_token(token):

	token.key = get(40)
	token.expiration = days_hence(1)
	token.invalid = False
	token.save()
	return token