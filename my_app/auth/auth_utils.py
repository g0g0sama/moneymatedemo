import re
from wtforms import ValidationError
from flask import request

def phone_number_validator(form, field):
    if not re.match(r'^\d{3}-\d{3}-\d{2}\d{2}$', field.data):
        raise ValidationError('Invalid phone number.')

def six_digits_validator(form, field, user):
    if not re.match(r'^\d{6}$', field.data):
        raise ValidationError('Please write six digits.')
    if (user.birth_year or user.birth_day or user.birth.month) in field.data:
        raise ValidationError('Your birth year, day or month cannot be in your password.')
    

def mernis_check(national_identity_number, firstname, lastname, birthyear):
    
    pass


def check_device():
    user_agent = request.headers.get('X-App-Type')

    return user_agent
