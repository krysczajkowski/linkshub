from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth import authenticate, login
import stripe
import json
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse

from .models import Customer, PremiumFreeTrial


stripe.api_key = "sk_test_51ImLvDFwBE1S4q2SI1GTEplWzXlrPpHkOAbZHjIZ5fon8deh1DuBCQXd7v46ZduiqrTNv0LuNhOyTUD0SXkUBc8L00pZQCKvFb"


def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = Customer()
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
    return render(request, 'premium/success.html')


def cancel(request):
    return render(request, 'premium/cancel.html')


@login_required
def join(request):
    try:
        if request.user.customer.membership:
            messages.info(request, 'You are already a premium user.')
            return redirect('membership')
    except Customer.DoesNotExist:
        pass

    # Get free trial status
    try:
        free_trial = PremiumFreeTrial.objects.get(user=request.user)

        display_free_trial = False
    except PremiumFreeTrial.DoesNotExist:
        display_free_trial = True

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 3.5
        membership_id = 'price_1JKldqFwBE1S4q2S8DJ3HxDI'
        # if request.method == 'GET' and 'membership' in request.GET:
        #     if request.GET['membership'] == 'one-time':
        #         membership = 'one-time'
        #         membership_id = 'price_1JKPBnFwBE1S4q2Se3fBAYDN'
        #         final_dollar = 4.5

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

@login_required
def membership(request):
    membership = False
    cancel_at_period_end = False
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
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'settings/membership.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})


@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')

# Add premium link click  
class start_free_trial(View):
    def post(self, request):
        try:
            get_trial = PremiumFreeTrial.objects.get(user=request.user)

            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409) 
        except PremiumFreeTrial.DoesNotExist:
            date = datetime.datetime.now() + datetime.timedelta(days=45)
            PremiumFreeTrial.objects.create(user=request.user, end_date=date)


        return JsonResponse({'success': True})