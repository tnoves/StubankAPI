from flask import Blueprint, request, jsonify
from app.database import db, ma
from app.sort_codes_api import SortCodesSchema

account_api = Blueprint('account_api', __name__)

# Setup Accounts model from database
class Accounts(db.Model):
    __tablename__ = 'Accounts'
    account_id = db.Column('AccountID', db.Integer, primary_key=True)
    account_number = db.Column('AccountNumber', db.Integer, unique=True)
    sort_code_id = db.Column('SortCodeID', db.Integer)

    def __init__(self, account_number, sort_code_id):
        self.account_number = account_number
        self.sort_code_id = sort_code_id

# Setup Accounts schema
class AccountsSchema(ma.Schema):
    sort_code = ma.Nested(SortCodesSchema)
    class Meta:
        additional = ('account_id', 'account_number', 'sort_code_id')

# Initialise schemas
accounts_schema = AccountsSchema()

# endpoint to get a specific account from id
@account_api.route('/account/<id>', methods=['GET'])
def get_account(id):
    account = Accounts.query.get(id)
    return accounts_schema.jsonify(account)

# endpoint to get account from a specific cards account number
@account_api.route('/account/card/<id>', methods=['GET'])
def get_account_from_card(account_number):
    account = Accounts.query.filter(Accounts.account_number == account_number)
    result = accounts_schema.dump(account)
    return jsonify(result)

# endpoint to update a specific account from id
@account_api.route('/account/<id>', methods=['PUT'])
def update_account(id):
    account = Accounts.query.get(id)
    account_number = request.json['account_number']
    sort_code_id = request.json['sort_code_id']

    account.account_number = account_number
    account.sort_code_id = sort_code_id

    db.session.commit()
    return accounts_schema.jsonify(account)

#endpoint to delete account
@account_api.route('/account/<id>', methods=['DELETE'])
def delete_account(id):
    account = Accounts.query.get(id)
    db.session.delete(account)
    db.session.commit()

    return accounts_schema.jsonify(account)