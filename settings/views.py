from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import imghdr
from imghdr import tests

from .forms import EditForm
from account.models import Profile
# Create your views here.
def index(request):
    return redirect('edit')

def edit(request):
    profile = Profile.objects.get(user=request.user)
    user = profile.user 

    username = user.username
    description = profile.description
    profile_pic = profile.image

    if request.method == 'POST':
        everything_ok = True

        image = request.FILES.get('imageField', False)
        username = request.POST['username']
        description = request.POST['description']
    
        # Username validation
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

        # Description validation
        if len(description) > 300:
            everything_ok = False
            error_msg = 'Description must be less than 300 characters.'

        # Image validation
        if image:
            # imghdr library has a bug (with jpeg files) and this code fixes it
            def test_jpeg1(h, f):
                """JPEG data in JFIF format"""
                if b'JFIF' in h[:23]:
                    return 'jpeg'


            JPEG_MARK = b'\xff\xd8\xff\xdb\x00C\x00\x08\x06\x06' \
                        b'\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'

            def test_jpeg2(h, f):
                """JPEG with small header"""
                if len(h) >= 32 and 67 == h[5] and h[:32] == JPEG_MARK:
                    return 'jpeg'


            def test_jpeg3(h, f):
                """JPEG data in JFIF or Exif format"""
                if h[6:10] in (b'JFIF', b'Exif') or h[:2] == b'\xff\xd8':
                    return 'jpeg'

            tests.append(test_jpeg1)
            tests.append(test_jpeg2)
            tests.append(test_jpeg3)
            # End of code that fix imghdr library

            image_extention = imghdr.what(image)
            
            print(image_extention)
            if image_extention is None:
                everything_ok = False
                error_msg = 'Please provide a valid image.'

        if everything_ok:
            user.username = username 
            user.save()

            if image:
                profile.image = image 
                profile_pic = profile.image
            
            profile.description = description
            profile.save()

            messages.success(request, 'Profile updated.')  
        else:
            messages.error(request, error_msg)  

    context = {
        'username': username, 
        'description': description,
        'image': profile_pic
    }

    return render(request, 'settings/edit.html', context)