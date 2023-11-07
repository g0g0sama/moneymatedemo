import re
from wtforms import ValidationError
def phone_number_validator(form, field):
    if not re.match(r'^\d{3}-\d{3}-\d{4}$', field.data):
        raise ValidationError('Invalid phone number.')

def six_digits_validator(form, field):
    if not re.match(r'^\d{6}$', field.data):
        raise ValidationError('Invalid six digits.')
