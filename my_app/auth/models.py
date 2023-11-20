from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, widgets, \
    TextAreaField
from wtforms.validators import InputRequired, EqualTo
from my_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    national_identity_number = db.Column(db.String(11), unique=True)
    phone_number = db.Column(db.String(20))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(20))
    password = db.Column(db.String())
    device_info = db.Column(db.String(255))
    """email = db.Column(db.String(255))
    phone_number_verified = db.Column(db.Boolean(), default=False)
    email_verified = db.Column(db.Boolean(), default=False)"""
    personal_info = db.relationship('Personal_info', backref='user', lazy=True, uselist=False)
    accounts = db.relationship('Account', backref='user', lazy=True)



    def __init__(self,national_identity_number, phone_number, firstname,
                  lastname, birthyear, password, device_info):
        self.national_identity_number = national_identity_number
        self.phone_number = phone_number
        self.firstname = firstname
        self.lastname = lastname
        self.birth_year = birthyear
        self.password = generate_password_hash(password)
        self.device_info = device_info
        """self.phone_number_verified = phone_number_verified
        self.email_verified = email_verified"""

    def __repr__(self):
        self.id = id
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
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




class Authfiles(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    id_front_file = db.Column(db.String(255), nullable=False)
    id_back_file = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __init__(self, id_front_file, id_back_file, user_id):
        self.id_front_file = id_front_file
        self.id_back_file = id_back_file
        self.user_id = user_id


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    pwdhash = db.Column(db.String())
    admin = db.Column(db.Boolean(), default=False)
    notes = db.Column(db.UnicodeText)
    roles = db.Column(db.String(4))

    def __init__(self, username, password, admin, roles='R'):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.admin = admin
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
    firstname = StringField('First name', [InputRequired()])
    lastname = StringField('Last name', [InputRequired()])
    birthyear = StringField('Birth year', [InputRequired()])
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
