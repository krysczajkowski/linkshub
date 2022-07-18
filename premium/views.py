from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth import authenticate, login
import stripe
import json
import time
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 

from .models import Customer, PremiumFreeTrial


stripe.api_key = "sk_test_51ImLvDFwBE1S4q2SI1GTEplWzXlrPpHkOAbZHjIZ5fon8deh1DuBCQXd7v46ZduiqrTNv0LuNhOyTUD0SXkUBc8L00pZQCKvFb"


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


@login_required(login_url='/authentication/login/')
def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:

        # If user rebuy premium delete the previous customer
        try:
            customer = Customer.objects.get(user=request.user)
            customer.delete()
        except Customer.DoesNotExist:
            pass   

        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)

        # Create customer object in db
        customer = Customer()
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()

        purchase_date = datetime.datetime.today().strftime('%Y-%m-%d')

        # Send success email
        email_subject = 'Thank you for purchasing LinksHub Premium.'
        # email_body = f'Hi {request.user.username}. Thank you for purchasing LinksHub Premium. Info dodatkowe jakies.'

        email_body = render_to_string('mails/premium-success.html', {'purchase_date': purchase_date})

        email = EmailMessage(
            email_subject,
            email_body,
            'czajkowski.biznes@gmail.com',
            [request.user.email],
        )

        email.content_subtype = 'html'
        EmailThread(email).start()

    return render(request, 'premium/success.html')


def cancel(request):
    return render(request, 'premium/cancel.html')


@login_required(login_url='/authentication/login/')
def join(request):
    try:
        if request.user.customer.membership:
            messages.info(request, 'You are already a premium user.')
            return redirect('membership')
    except Customer.DoesNotExist:
        pass


    # Check if user had free trial activated before
    try:
        free_trial = PremiumFreeTrial.objects.get(user=request.user)

        free_trial_exist = True
    except PremiumFreeTrial.DoesNotExist:
        free_trial_exist = False

    # Check if user bought premium before or uses it now
    try:
        customer = Customer.objects.get(user=request.user)

        customer_exist = True
    except Customer.DoesNotExist:
        customer_exist = False 

    # Check if display free trial button
    if free_trial_exist or customer_exist:
        display_free_trial = False 
    else:
        display_free_trial = True


    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 3.5
        membership_id = 'price_1JKldqFwBE1S4q2S8DJ3HxDI'

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/premium/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/premium/cancel',
        )

        context = {
            'final_dollar': final_dollar,
            'session_id': session.id,
            'display_free_trial': display_free_trial
        }

        return render(request, 'premium/join.html', context)

@login_required(login_url='/authentication/login/')
def membership(request):
    membership = False
    cancel_at_period_end = False

    context = {}

    # Check if user has premium membership
    if Customer.objects.filter(user=request.user).exists():
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

        current_period_end = datetime.datetime.fromtimestamp(subscription.current_period_end)
        pretty_current_period_end = f"{current_period_end:%Y-%m-%d %H:%M}"
        context['current_period_end'] = pretty_current_period_end

        # Check if they canceled premium
        if subscription.cancel_at_period_end:
            premium_cancel_at = datetime.datetime.fromtimestamp(subscription.cancel_at)
            pretty_premium_cancel_at = f"{premium_cancel_at:%Y-%m-%d %H:%M}"
            context['premium_cancel_at'] = pretty_premium_cancel_at

    # User canceled premium membership
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
                purchase_date = datetime.datetime.fromtimestamp(subscription.created)
                pretty_purchase_date = f"{purchase_date:%Y-%m-%d %H:%M}" 
                context['purchase_date'] = pretty_purchase_date

            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False

    context['membership'] = membership
    context['cancel_at_period_end'] = cancel_at_period_end

    return render(request, 'settings/membership.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/authentication/login/')
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False

            # PREMIUM EXPIRED
            # Send email to user about expired premium
            email_subject = 'Your LinksHub Premium has expired.'

            email_body = render_to_string('mails/premium-expired.html', {'username': customer.user.username})

            email = EmailMessage(
                email_subject,
                email_body,
                'czajkowski.biznes@gmail.com',
                [customer.user.email],
            )

            email.content_subtype = 'html'
            EmailThread(email).start()
        else:
            customer.membership = True


        # PREMIUM IS ABOUT TO EXPIRE
        if subscription.cancel_at_period_end:
            # Send email to user about expired premium
            email_subject = 'Your LinksHub Premium is about to expire.'
            
            expire_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(subscription.cancel_at))

            email_body = render_to_string('mails/premium-about-to-expire.html', {'username': customer.user.username, 'expire_date': expire_date})

            email = EmailMessage(
                email_subject,
                email_body,
                'czajkowski.biznes@gmail.com',
                [customer.user.email],
            )

            email.content_subtype = 'html'
            EmailThread(email).start()


        # Set cancel at period time value
        customer.cancel_at_period_end = subscription.cancel_at_period_end

        customer.save()
    return HttpResponse('completed')

# Add premium link click  
class start_free_trial(View):
    def post(self, request):
        date = datetime.datetime.now() + datetime.timedelta(days=45)

        try:
            get_trial = PremiumFreeTrial.objects.get(user=request.user)

            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409) 
        except PremiumFreeTrial.DoesNotExist:
            PremiumFreeTrial.objects.create(user=request.user, end_date=date)
        
        return JsonResponse({'end_date': date})

@login_required(login_url='/authentication/login/')
def free_trial_success(request):
    return render(request, 'premium/free_trial_success.html')