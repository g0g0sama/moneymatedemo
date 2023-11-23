from flask import Blueprint, jsonify, request
from flask_restx import Resource, Api, fields
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import decode_token
from .utils import get_account_balance, mmtommtransaction, save_transaction
from ..auth.models import User
from my_app import db
from datetime import datetime
from .models import Account
from my_app import db, login_manager, admin_login_manager, app, ALLOWED_EXTENSIONS, jwt, jwt_redis_blocklist, ACCESS_EXPIRES, api

business = Blueprint('business', __name__)



@api.route('/user/initialize_account')
class Intitialize_account(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        existing_user = User.query.filter_by(national_identity_number=current_user).first()
        if existing_user.is_active:
            db.session.add(Account(user_id=existing_user.id, currency="TRY"))
            db.session.commit()
        else:
            return {"message": "Account"}, 400
        return {'hello': 'world'}

@api.route('/user/create_account')
class Create_account(Resource):
    @jwt_required()
    def get(self, currency):
        current_user = get_jwt_identity()
        existing_user = User.query.filter_by(national_identity_number=current_user).first()
        if existing_user:
            db.session.add(Account(user_id=existing_user.id, currency=currency))
            db.commit()
        else:
            return {"message": "Account"}, 400
        return {'hello': 'world'}



@api.route('/user/<int:id>/m2mtransaction')

class Mmtommtransaction(Resource):
    @jwt_required()
    def post(self, sender_account_id,receiver_account_id,amount,transaction_date):
        transaction = mmtommtransaction(sender_account_id,receiver_account_id,amount,transaction_date)
        if transaction:
            save_transaction(sender_account_id,receiver_account_id,amount,transaction_date)
        else:   
            return {"message": "Insufficient balance"}, 400

@api.route('/user/<int:id>/<string:currency>/<int:account_id>/balance')

class Account_balance(Resource):
    @jwt_required()
    def get(self, id, currency, account_id):
        current_user = get_jwt_identity()
        existing_user = User.query.filter_by(national_identity_number=current_user).first()
        if current_user.id != id:
            return {"message": "User does not exist"}, 400
        return get_account_balance(id, currency)
    

@api.route("/user/transaction_history")

class Users(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        existing_user = User.query.filter_by(national_identity_number=current_user).first()
        if not existing_user:
            return {"message": "User does not exist"}, 400
        return jsonify(existing_user.transaction_history)

