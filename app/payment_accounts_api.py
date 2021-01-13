from flask import Blueprint, request
from app.database import db, ma
from app.user_api import UserDetailsSchema
from app.card_api import AccountsSchema

payment_accounts_api = Blueprint('payment_accounts_api', __name__)

# Setup PaymentAccount model from database
class PaymentAccounts(db.Model):
    __tablename__ = 'PaymentAccount'
    payment_account_id = db.Column('PaymentAccountID', db.Integer, primary_key=True)
    account_id = db.Column('AccountID', db.Integer)
    user_details_id = db.Column('UserDetailsID', db.Integer)

    def __init__(self, account_id, user_details_id):
        self.account_id = account_id
        self.user_details_id = user_details_id

# Setup PaymentAccount schema
class PaymentAccountsSchema(ma.Schema):
    account = ma.Nested(AccountsSchema)
    user_details = ma.Nested(UserDetailsSchema)
    class Meta:
        additional = ('payment_account_id', 'account_id', 'user_details_id')

# Initialise schemas
payment_account_schema = PaymentAccountsSchema()

@payment_accounts_api.route('/payment_account/', methods=['POST'])
def create_payment_account():
    account_id = request.json['account_id']
    user_details_id = request.json['user_details_id']

    try:
        payment_account = PaymentAccounts(account_id=account_id, user_details_id=user_details_id)

        db.session.add(payment_account)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return payment_account_schema.jsonify(payment_account)

# endpoint to get a specific payment account from id
@payment_accounts_api.route('/payment_account/<id>', methods=['GET'])
def get_payment_account(id):
    payment_account = PaymentAccounts.query.get(id)
    return payment_account_schema.jsonify(payment_account)

# endpoint to update a specific payment account from id
@payment_accounts_api.route('/payment_account/<id>', methods=['PUT'])
def update_payment_account(id):
    try:
        payment_account = PaymentAccounts.query.get(id)
        account_id = request.json['account_id']
        user_details_id = request.json['user_details_id']

        payment_account.account_id = account_id
        payment_account.user_details_id = user_details_id

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return payment_account_schema.jsonify(payment_account)

#endpoint to delete payment account
@payment_accounts_api.route('/transaction/<id>', methods=['DELETE'])
def delete_payment_account(id):
    payment_account = PaymentAccounts.query.get(id)
    db.session.delete(payment_account)
    db.session.commit()

    return payment_account_schema.jsonify(payment_account)