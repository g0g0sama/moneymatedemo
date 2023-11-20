from my_app import api
from flask_restx import Resource, Api, fields
# from .info_utils import get_account_balance, m2mtransaction, save_transaction
from flask import jsonify, Blueprint
# from auth.models import User

personal_info = Blueprint('personal_info', __name__)

@api.route('/user/<int:id>')
class Userhome(Resource):
    def get(self, id):
        existing_user = User.query.filter_by(id=id).first()
        if not existing_user:
            return {"message": "User does not exist"}, 400
        return jsonify(existing_user)

@api.route('/user/<int:id>/m2mtransaction')
class Mmtommtransaction(Resource):
    def post(self, sender_account_id,receiver_account_id,amount,transaction_date):
        transaction = m2mtransaction(sender_account_id,receiver_account_id,amount,transaction_date)
        if transaction:
            save_transaction(sender_account_id,receiver_account_id,amount,transaction_date)
        else:   
            return {"message": "Insufficient balance"}, 400

@api.route('/user/<int:id>/<string:currency>/balance')
class Account_balance(Resource):
    def get(self, id, currency):
        return get_account_balance(id, currency)
    

@api.route("/users/<int:id>/transaction_history")

class Users(Resource):
    def get(self, id):
        existing_user = User.query.filter_by(id=id).first()
        if not existing_user:
            return {"message": "User does not exist"}, 400
        return jsonify(existing_user.transaction_history)