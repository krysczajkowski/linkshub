from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth.models import User

def username_validation(request, username, everything_ok, error_msg):
    if not str(username).isalnum():
        everything_ok = False
        error_msg = 'Username should only contain alphanumeric characters.'

    if User.objects.filter(username=username).exists():
        if request.user.username != username:
            everything_ok = False
            error_msg = 'Sorry, this username is already in use.'

    if len(username) < 2 or len(username) > 80:
        everything_ok = False
        error_msg = 'Username must be between 2 or 80 characters.'

    return {'everything_ok': everything_ok, 'error_msg': error_msg}


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))

token_generator = AppTokenGenerator()
