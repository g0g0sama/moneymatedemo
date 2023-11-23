from .models import Account
from .models import Mmtomm
from my_app import db


def mmtommtransaction(sender_account_id, receiver_account_id, amount, curreny, transaction_date):
    sender_account = Account.query.filter_by(curreny=curreny, user_id= sender_account_id).first()
    receiver_account = Account.query.filter_by(curreny=curreny, user_id = receiver_account_id).first()
    if sender_account is None:
        return f"Please create an {curreny} account first."
    if receiver_account is None:
        return f"Wrong account number."
    sender_account_id.balance -= amount
    if sender_account_id.balance < 0:
        return "insufficient balance"
    else:
        receiver_account_id.balance += amount
        transaction = Transaction(sender_account_id,receiver_account_id,amount,transaction_date)
        db.session.add(transaction)
        db.session.commit()
        return True
    

def get_account_balance(id, currency, account_id):
    account = Account.query.filter_by(user_id=id, currency=currency).first()
    if account is None:
        return False
    return account.balance


def save_transaction(sender_account_id,receiver_account_id,amount,transaction_date):
    transaction = Transaction(sender_account_id,receiver_account_id,amount,transaction_date)
    db.session.add(transaction)
    db.session.commit()
    return True
