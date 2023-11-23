from my_app import db
from datetime import datetime


class Account(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False) 
    balance = db.Column(db.Float, nullable=True, default= 0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, nullable=True, default= 19000, unique=True, autoincrement=True)


class Account_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curreny = db.Column(db.String(255), nullable=True, default= "TRY")

class Mmtomm(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    sender_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    receiver_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=True, default= None)
    transaction_date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow())
    success = db.Column(db.Boolean, nullable=True, default= False)
    transaction_id = db.Column(db.Integer, nullable=True, default= None, unique=True, autoincrement=True)
    Transaction_type = db.Column(db.Integer, db.ForeignKey('transaction_type.id'), nullable=False)
    def __init__(self,sender_account_id,receiver_account_id,amount,transaction_date):
        self.sender_account_id = sender_account_id
        self.receiver_account_id = receiver_account_id
        self.amount = amount
        self.transaction_date = transaction_date

class Transaction_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(255), nullable=True, default= None)

class Transaction_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_account_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.Integer, db.ForeignKey('transaction_type.id'), nullable=False)
    transaction_id = db.Column(db.Integer, nullable=False)
    transaction_amount = db.Column(db.Float, nullable=True, default= None)
    transaction_date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow())