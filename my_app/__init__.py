from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from os.path import join, dirname, realpath
from flask_jwt_extended import JWTManager
from datetime import timedelta
import redis
from flask_restx import  Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'

    }
}

ACCESS_EXPIRES = timedelta(minutes=5)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://goksucan:123456789g@127.0.0.1/fastapi'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'

api = Api(app, authorizations=authorizations, security="apikey")

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 3 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

jwt = JWTManager(app)

db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

admin_login_manager = LoginManager()
admin_login_manager.init_app(app)
admin_login_manager.login_view = 'auth.admin_login'

import my_app.auth.views as views
admin = Admin(app, index_view=views.MyAdminIndexView())
admin.add_view(views.UserAdminView(views.AdminUser, db.session))

from my_app.auth.views import auth
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

