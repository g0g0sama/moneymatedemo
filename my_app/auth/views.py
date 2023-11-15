from functools import wraps
from werkzeug.security import generate_password_hash
from flask import request, render_template, flash, redirect, url_for, \
    session, Blueprint, g, abort, jsonify
from flask_login import current_user, login_user, logout_user, \
    login_required
from wtforms import PasswordField
from my_app import db, login_manager, admin_login_manager, app, ALLOWED_EXTENSIONS, jwt, jwt_redis_blocklist, ACCESS_EXPIRES, api
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.form import rules
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import ActionsMixin
from my_app.auth.models import User, AdminUser, Personal_info,Authfiles, RegistrationForm, LoginForm, AdminLoginForm, \
    AdminUserCreateForm, AdminUserUpdateForm, generate_password_hash, \
    CKTextAreaField
from werkzeug.utils import secure_filename
import os
from . import mernis
from .auth_utils import check_device
from flask import Response

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
import datetime
from flask_restx import Resource, Api, fields
auth = Blueprint('auth', __name__)



def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@admin_login_manager.user_loader
def load_admin(id):
    return AdminUser.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')


"""
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Your are already logged in.', 'info')
        return redirect(url_for('auth.home'))
    form = RegistrationForm()

    if form.validate_on_submit(): 

        national_identity_number = request.form.get('national_identity_number')
        phone_number = request.form.get('phone_number')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthyear = request.form.get('birthyear')
        existing_phone_number = User.query.filter_by(phone_number=phone_number).first()
        existing_national_identity_number = User.query.filter_by(national_identity_number=national_identity_number).first()
        password = request.form.get('password')
        if existing_phone_number or existing_national_identity_number:
            flash(
                'This phone number has been already taken. Try another one.',
                'warning'
            )
            return render_template('register.html', form=form)
        user = User(national_identity_number=national_identity_number, phone_number=phone_number, birthyear=birthyear, firstname=firstname, lastname=lastname, password =password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('auth.login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)
"""



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Your are already logged in.', 'info')
    firstname = request.get_json()['firstname']
    lastname = request.get_json()['lastname']
    identity_number = request.get_json()['identity_number']
    birthyear = request.get_json()['birthyear']
    password = request.get_json()['password']
    phone_number = request.get_json()['phone_number']
    device_info = request.get_json()['device_info']
    existing_phone_number = User.query.filter_by(phone_number=phone_number).first()
    existing_national_identity_number = User.query.filter_by(national_identity_number=identity_number).first()
    if existing_phone_number or existing_national_identity_number:

        return "false"
    #Response(response='This phone number has been already taken. Try another one.',status=500)
    user = User(national_identity_number=identity_number, phone_number=phone_number, birthyear=birthyear, firstname=firstname, 
                lastname=lastname, password =password, device_info=device_info)
    db.session.add(user)
    db.session.commit()
    flash('You are now registered. Please login.', 'success')
    return  "true" # Response(response='Successful.',status=200)
    

@auth.route('/mernis-check', methods=['GET', 'POST'])
def mernis_check():
    firstname = request.get_json()['firstname']
    lastname = request.get_json()['lastname']
    identity_number = request.get_json()['identity_number']
    birthyear = request.get_json()['birthyear']
    if mernis.mernis_check(identity_number, firstname, lastname, birthyear) == False:
        return "false"
    else:
        return "true"



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "true", 200

    identity_number = request.get_json()['identity_number']
    password = request.get_json()['password']
    device_info = request.get_json()['device_info']
    existing_user = User.query.filter_by(national_identity_number=identity_number).first()
    user_agent = check_device()
    if device_info != existing_user.device_info:
        print("why1")
        return "false", 400
    if not (existing_user and existing_user.check_password(password)):
        print("why2")
        return "false", 400
    
    if user_agent == "mobile":
        login_user(existing_user)

        return {"user_id":existing_user.id, "firstname":existing_user.firstname, "lastname": existing_user.lastname, "identity_number":existing_user.national_identity_number, "phone_number": existing_user.phone_number}, 200
    else:
        login_user(existing_user )
        return redirect(url_for('auth.home'))
    
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@auth.route('/jwtlogin', methods=['GET', 'POST'])
def jwtlogin():
    identity_number = request.get_json()['identity_number']
    password = request.get_json()['password']
    existing_user = User.query.filter_by(national_identity_number=identity_number).first()
    user_agent = check_device()
    if not (existing_user and existing_user.check_password(password)):
        return "false", 400
    
    if user_agent == "mobile":
        access_token = create_access_token(identity=identity_number, fresh=datetime.timedelta(minutes=5))
        refresh_token = create_refresh_token(identity=identity_number)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    else:
        access_token = create_access_token(identity=identity_number, fresh=datetime.timedelta(minutes=5))
        refresh_token = create_refresh_token(identity=identity_number)
        return jsonify(access_token=access_token, refresh_token=refresh_token) 
    

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)
    
@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    existing_user = User.query.filter_by(national_identity_number=current_user).first()
    return jsonify({"user_id":existing_user.id, "firstname":existing_user.firstname, "lastname": existing_user.lastname, "identity_number":existing_user.national_identity_number, "phone_number": existing_user.phone_number}), 200
   

@app.route("/jwtlogout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    # Returns "Access token revoked" or "Refresh token revoked"
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))



@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('admin-home.html'))

    form = AdminLoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = AdminUser.query.filter_by(username=username).first()

        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid phone number or password. Please try again.', 'danger')
            return render_template('admin-login.html', form=form)

        login_user(existing_user)
        flash('You have successfully logged in.', 'success')
        return render_template('admin-home.html')

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('admin-login.html', form=form)



@auth.route('/admin')
@login_required
@admin_login_required
def home_admin():
    return render_template('admin-home.html')


@auth.route('/admin/users-list')
@login_required
@admin_login_required
def users_list_admin():
    users = User.query.all()
    personal_infos = Personal_info.query.all()
    return render_template('users-list-admin.html', users=users, personal_infos=personal_infos)





@auth.route('/admin/create-user', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_create_admin():
    form = AdminUserCreateForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = form.admin.data
        existing_username = AdminUser.query.filter_by(username=username).first()
        if existing_username:
            flash(
                'This phone_number has been already taken. Try another one.',
                'warning'
            )
            return render_template('register.html', form=form)
        user = AdminUser(username, password, admin)
        db.session.add(user)
        db.session.commit()
        flash('New User Created.', 'info')
        return redirect(url_for('auth.users_list_admin'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('user-create-admin.html', form=form)


@auth.route('/admin/update-user/<id>', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_update_admin(id):
    user = User.query.get(id)
    form = AdminUserUpdateForm(
        phone_number=user.phone_number,
  
    )

    if form.validate_on_submit():
        phone_number = form.phone_number.data
        User.query.filter_by(id=id).update({
            'phone_number': phone_number,
        })

        db.session.commit()
        flash('User Updated.', 'info')
        return redirect(url_for('auth.users_list_admin'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('user-update-admin.html', form=form, user=user)


@auth.route('/admin/delete-user/<id>')
@login_required
@admin_login_required
def user_delete_admin(id):
    user = AdminUser.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted.', 'info')
    return redirect(url_for('auth.users_list_admin'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()


class UserAdminView(ModelView, ActionsMixin):
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'admin')
    column_exclude_list = ('pwdhash',)
    form_excluded_columns = ('pwdhash',)
    form_edit_rules = (
        'username', 'admin', 'roles', 'notes',
        rules.Header('Reset Password'),
        'new_password', 'confirm'
    )
    form_create_rules = (
        'username', 'admin', 'roles', 'notes', 'password'
    )
    form_overrides = dict(notes=CKTextAreaField)

    create_template = 'edit.html'
    edit_template = 'edit.html'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.new_password = PasswordField('New Password')
        form_class.confirm = PasswordField('Confirm New Password')
        return form_class

    def create_model(self, form):
        if 'C' not in current_user.roles:
            flash('You are not allowed to create users.', 'warning')
            return
        model = self.model(
            form.phone_number.data, form.password.data, form.admin.data,
            form.notes.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    def update_model(self, form, model):
        if 'U' not in current_user.roles:
            flash('You are not allowed to edit users.', 'warning')
            return
        form.populate_obj(model)
        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash('Passwords must match')
                return
            model.pwdhash = generate_password_hash(
                form.new_password.data)
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()

    def delete_model(self, model):
        if 'D' not in current_user.roles:
            flash('You are not allowed to delete users.', 'warning')
            return
        super(UserAdminView, self).delete_model(model)

    def is_action_allowed(self, name):
        if name == 'delete' and 'D' not in current_user.roles:
            flash('You are not allowed to delete users.', 'warning')
            return False
        return True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/file_upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pepo = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.id}/")
            f = os.makedirs(pepo, exist_ok=True)
            file.save(os.path.join(pepo, filename))

            user_file = Authfiles(id_front_file= pepo, user_id=current_user.id, id_back_file=pepo)
            db.session.add(user_file)
            db.session.commit()
            return  "success"
    return render_template('file-upload.html')



@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}



resource_fields = api.model('login_fields', {
    'identity_number': fields.String,
    "password": fields.String,
})
@api.route('/jwtlogin1')
class Jwtlogin(Resource):
    @api.expect(resource_fields)
    def post(self):
        identity_number = request.get_json()['identity_number']
        password = request.get_json()['password']
        existing_user = User.query.filter_by(national_identity_number=identity_number).first()
        user_agent = check_device()
        if not (existing_user and existing_user.check_password(password)):
            return "false", 400
        
        if user_agent == "mobile":
            access_token = create_access_token(identity=identity_number, fresh=datetime.timedelta(minutes=5))
            refresh_token = create_refresh_token(identity=identity_number)
            return jsonify(access_token=access_token, refresh_token=refresh_token)

        else:
            access_token = create_access_token(identity=identity_number, fresh=datetime.timedelta(minutes=5))
            refresh_token = create_refresh_token(identity=identity_number)
            return jsonify(access_token=access_token, refresh_token=refresh_token) 
        


auth_resource_fields = api.model('auth_fields', {
    'access_token': fields.String,
})

@api.route("/userhome")

class Protected(Resource):    
    @jwt_required()
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        existing_user = User.query.filter_by(national_identity_number=current_user).first()
        return jsonify({"user_id":existing_user.id, "firstname":existing_user.firstname, "lastname": existing_user.lastname, "identity_number":existing_user.national_identity_number, "phone_number": existing_user.phone_number})
    