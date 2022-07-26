from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

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

def send_acc_activation_email(request, user, email):
    # Sending email
    email_subject = 'Activate your account'

    # Path to view
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    domain = get_current_site(request).domain
    link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

    activate_url = 'http://' + domain + link

    email_body = render_to_string('mails/verify-email.html', {'username': user.username, 'verify_email_url': activate_url})

    emailMsg = EmailMessage(
        email_subject,
        email_body,
        'czajkowski.biznes@gmail.com',
        [email],
    )

    return emailMsg
