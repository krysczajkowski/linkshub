import imghdr
from imghdr import tests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import uuid
import hashlib

from .views import LinkAnimation
 
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def validate_image(image, everything_ok, error_msg):
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
    
    if image_extention is None:
        everything_ok = False
        error_msg = 'Please provide a valid image.'
    
    return {'everything_ok': everything_ok, 'error_msg': error_msg}


def validate_link_form(title, description, url, image, animation):
    everything_ok = True 
    error_msg = ''

    if len(title) < 1 or len(title) > 70:
        everything_ok = False 
        error_msg = 'Title length must be between 1 and 70 characters.'

    if len(description) > 150:
        everything_ok = False 
        error_msg = 'Description length can not be over 150 characters.'
    
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError as exception:
        everything_ok = False
        error_msg = 'Please provide valid URL.'
    
    if image:
        validated_image = validate_image(image, everything_ok, error_msg)
        everything_ok = validated_image['everything_ok']
        error_msg = validated_image['error_msg']

    #animations = ['none', 'pulse', 'jump', 'waggle', 'sheen', 'spin']

    #if animation not in animations:
    #    everything_ok = False 
    #    error_msg = 'Please choose correct animation.'

    try:
        chosen_animation = LinkAnimation.objects.get(name=animation)
    except LinkAnimation.DoesNotExist:
        everything_ok = False 
        error_msg = 'Please choose correct animation.'  
        
    return {'everything_ok': everything_ok, 'error_msg': error_msg}
