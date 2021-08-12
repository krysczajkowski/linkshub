from django.contrib.gis.geoip2 import GeoIP2

from premium.models import Customer 

# Get visit of your profile date
def get_view_date(view):
    return view.date

# Get ip 
def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip


def get_location(request):
    # Get visitor's ip
    ip = get_ip(request)

    # Get visitors location
    try:    
        g = GeoIP2()
        country = g.country('5.172.234.51')['country_name'] # 128.101.101.101 -> ip
        city = g.city('5.172.234.51')['city']

        if country is None:
            country = 'Unknown'
        elif city is None:
            city = 'Unknown'

    except: # gaierror, AddressNotFoundError, TypeError, 
        country = 'Unknown'
        city = 'Unknown'

    return {'country': country, 'city': city}

def get_membership(request):
    try: 
        membership = Customer.objects.get(user=request.user).membership
    except:
        membership = 0

    return membership