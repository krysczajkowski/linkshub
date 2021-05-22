from django.shortcuts import render, redirect
from django.views import View
import json
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
import requests


from .utils import token_generator

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html', {'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

    def post(self, request):
        # reCAPTCHA validation
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }

        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        print(result)

        if result['success']:
            # Get user data
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            context = {
                'fieldValues': request.POST
            }

            everything_ok = True

            # Username validation
            if not str(username).isalnum():
                everything_ok = False
                error_msg = 'Username should only contain alphanumeric characters.'

            if User.objects.filter(username=username).exists():
                everything_ok = False
                error_msg = 'Sorry, this username is already in use.'

            # Email validaiton
            if not validate_email(email):
                everything_ok = False
                error_msg = 'Email is invalid.'

            if User.objects.filter(email=email).exists():
                everything_ok = False
                error_msg = 'This email is already taken.'

            if len(password) < 6 or len(password) > 40:
                everything_ok = False
                error_msg = 'Password must be between 6 or 40 characters.'

            if everything_ok == True:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                email_subject = 'Activate your account'

                # Path to view
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = 'http://' + domain + link

                email_body = f'Hi {user.username}. Please use this link to verify your account. {activate_url}'

                '''
                email = send_mail(
                    email_subject,
                    email_body,
                    'czakowski.biznes@gmail.com',
                    [email],
                )
                '''
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'czajkowski.biznes@gmail.com',
                    [email],
                )
                EmailThread(email).start()

                #email.send(fail_silently=False) # show errors if there are any

                messages.success(request, 'Account created. Activate your account in gmail.')
            else:
                messages.error(request, error_msg)

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        return render(request, 'authentication/register.html', {'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})


class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not token_generator.check_token(user, token):
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully! You can log in now.')
            return redirect('login')

        except Exception as e:
            raise

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username)

                    if not request.POST.get('remember_me', False):
                        request.session.set_expiry(0)
                        request.session.modified = True

                else:
                    messages.error(request, 'Account is not active, please check your email.')
            else:
                messages.error(request, 'Invalid credentials, try again.')
        else:
            messages.error(request, 'Please fill all fields.')

        return redirect('profile')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email.')

        user = User.objects.filter(email=email)

        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain

            link = reverse('reset-user-password', kwargs={'uidb64': uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})

            reset_url = 'http://' + domain + link

            email_body = f'Hi {user[0].username}. Please use this link to reset your password. {reset_url}'

            email_subject = 'Password Reset Instructions'

            '''
            email = send_mail(
                email_subject,
                email_body,
                'czakowski.biznes@gmail.com',
                [email],
            )
            '''
            email = EmailMessage(
                email_subject,
                email_body,
                'czajkowski.biznes@gmail.com',
                [email],
            )
            EmailThread(email).start()

            messages.success(request, 'Log in to your gmail, biatch.')
        else:
            messages.error(request, "This email does not exist")

        context = {
            'values': request.POST
        }

        return render(request, 'authentication/reset-password.html', context)


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(id=user_id)

            # Check if user didn't use this link before
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password reset link is invalid.')
                return render(request, 'authentication/reset-password.html')
        except Exception as identifier:
            pass

        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        everything_ok = 1
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            everything_ok = 0
            messages.error(request, 'Passwords do not match.')

        if len(password) < 6:
            everything_ok = 0
            messages.error(request, 'Password is too short.')

        if everything_ok == 1:
            try:
                user_id = force_text(urlsafe_base64_decode(uidb64))

                user = User.objects.get(id=user_id)

                user.set_password(password)
                user.save()

                messages.success(request, 'Password changed.')
                return redirect('login')
            except Exception as identifier:
                messages.error(request, 'Sorry, something went wrong. Please try again.')

        return render(request, 'authentication/set-new-password.html', context)

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, this username is already in use.'}, status=409)

        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, this email is already in use.'}, status=409)

        return JsonResponse({'email_valid': True})


class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        if len(password) < 6 or len(password) > 40:
            return JsonResponse({'password_error': 'Password must be between 6 or 40 characters.'}, status=409)

        return JsonResponse({'password_valid': True})
