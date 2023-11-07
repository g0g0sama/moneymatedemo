from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, widgets, \
    TextAreaField
from wtforms.validators import InputRequired, EqualTo
from my_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    national_identity_number = db.Column(db.String(11))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(255))
    pwdhash = db.Column(db.String())
    """admin = db.Column(db.Boolean())
    notes = db.Column(db.UnicodeText)
    roles = db.Column(db.String(4))"""



    def __init__(self,national_identity_number, phone_number, email,  password):
        self.national_identity_number = national_identity_number
        self.phone_number = phone_number
        self.email = email
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def is_admin(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Personal_info(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    first_name = db.Column(db.String(255))
    surname = db.Column(db.String(255)) 
    address = db.Column(db.Float)
    country = db.Column(db.String(255)) #find the iso codes and country list by language
    city = db.Column(db.String(255)) #find the cities by country
    ##national_identity = db.Column(db.enum("TC vatandaşı", "Yabancı uyruklu"), default="TC vatandaşı")
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, first_name, surname, address, country, city, national_identity, birth_year, birth_month, birth_day):
        self.first_name = first_name
        self.surname = surname
        self.address = address
        self.country = country
        self.city = city
        self.national_identity = national_identity
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    pwdhash = db.Column(db.String())
    admin = db.Column(db.Boolean(), default=False)
    notes = db.Column(db.UnicodeText)
    roles = db.Column(db.String(4))

    def __init__(self, username, password, admin, notes='', roles='R'):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.admin = admin
        self.notes = notes
        self.roles = self.admin and roles or ''


    def is_admin(self):
        return self.admin

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class RegistrationForm(FlaskForm):
    national_identity_number = StringField('National Identity Number', [InputRequired()])
    phone_number = StringField('Phone number', [InputRequired()])
    email = StringField('Email', [InputRequired()]) 

    password = PasswordField(
        'Password', [
            InputRequired(), EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(FlaskForm):
    phone_number = StringField('Phone number', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


class AdminLoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])



class AdminUserCreateForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    admin = BooleanField('Is Admin ?')


class AdminUserUpdateForm(FlaskForm):
    phone_number = StringField('Phone number', [InputRequired()])
    

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()
