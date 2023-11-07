from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://goksucan:123456789g@127.0.0.1/fastapi'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
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
