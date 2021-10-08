from django.shortcuts import render

# Create your views here.
def terms(request):
    return render(request, 'sitepolicy/terms.html')

def privacy_policy(request):
    return render(request, 'sitepolicy/privacy-policy.html')