import datetime
from my_app import db
from .models import Account, Transaction
from auth.models import User


def create_new_account(id, currency):
    user = User.query.filter_by(id=id).first()
    if user.account.currency == "currency":
        return False
    account = Account(user_id=id, currency=currency)
    db.session.add(account)
    db.session.commit()
    return True


