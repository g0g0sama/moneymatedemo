import re
from wtforms import ValidationError
from flask import request

def phone_number_validator(number):
    if not re.match(r'^\d{3}-\d{3}-\d{2}\d{2}$', number):
        raise ValidationError('Invalid phone number.')

def password_validator(field, user):
    if not re.match(r'^\d{6}$', field):
        raise ValidationError('Please write six digits.')
    if user.birthyear in field:
        raise ValidationError('Your password cannot contain your birthyear.')
    if  re.match(r'(\d)\1{5}', field):
        raise ValidationError('Your password cannot contain repeated digits.')
    if re.match(r'^\d{6}$', field):
        raise ValidationError('Your password cannot contain sequential digits.')
    return True

def mernis_check(national_identity_number, firstname, lastname, birthyear):
    
    pass


def check_device():
    user_agent = request.headers.get('X-App-Type')
    # device info can be merged together.
    return user_agent
