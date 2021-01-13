from flask import Blueprint, request, jsonify
from app.database import db, ma
from app.card_api import CardsSchema
from app.payment_accounts_api import PaymentAccountsSchema

transaction_api = Blueprint('transaction_api', __name__)

# Setup Transactions model from database
class Transactions(db.Model):
    __tablename__ = 'Transactions'
    id = db.Column('TransactionID', db.Integer, primary_key=True)
    card_number = db.Column('16DigitCardNo', db.Integer)
    balance = db.Column('Balance', db.Integer)
    date = db.Column('Date', db.Date)
    payment_account_id = db.Column('PaymentAccountID', db.Integer)
    payment_amount = db.Column('PaymentAmount', db.Integer)
    payment_type = db.Column('PaymentType', db.String(100))

    def __init__(self, card_number, balance, date, payment_account_id, payment_amount, payment_type):
        self.card_number = card_number
        self.balance = balance
        self.date = date
        self.payment_account_id = payment_account_id
        self.payment_amount = payment_amount
        self.payment_type = payment_type

# Setup Transaction schema
class TransactionSchema(ma.Schema):
    card = ma.Nested(CardsSchema)
    payment_account = ma.Nested(PaymentAccountsSchema)
    class Meta:
        additional = ('id', 'card_number', 'balance', 'date', 'payment_account_id', 'payment_amount', 'payment_type')

# Initialise schemas
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

# endpoint to create a transaction
@transaction_api.route('/transaction/', methods=['POST'])
def create_transaction():
    card_number = request.json['card_number']
    balance = request.json['balance']
    date = request.json['date']
    payment_account_id = request.json['payment_account_id']
    payment_amount = request.json['payment_amount']
    payment_type = request.json['payment_type']

    try:
        transaction = Transactions(card_number=card_number, balance=balance, date=date,
                                   payment_account_id=payment_account_id, payment_amount=payment_amount,
                                   payment_type=payment_type)

        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return transaction_schema.jsonify(transaction)

# endpoint to get a specific transaction from id
@transaction_api.route('/transaction/<id>', methods=['GET'])
def get_transaction(id):
    transaction = Transactions.query.get(id)
    return transaction_schema.jsonify(transaction)

# endpoint to get all transactions for specified card
@transaction_api.route('/transaction/card/<id>', methods=['GET'])
def get_all_transactions(card_number):
    transactions = Transactions.query.filter(Transactions.card_number == card_number)
    result = transactions_schema.dump(transactions)
    return jsonify(result)

# endpoint to update a specific transaction from id
@transaction_api.route('/transaction/<id>', methods=['PUT'])
def update_transaction(id):
    try:
        transaction = Transactions.query.get(id)
        card_number = request.json['card_number']
        balance = request.json['balance']
        date = request.json['date']
        payment_amount = request.json['payment_amount']
        payment_type = request.json['payment_type']

        transaction.card_number = card_number
        transaction.balance = balance
        transaction.date = date
        transaction.payment_amount = payment_amount
        transaction.payment_type = payment_type

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return transaction_schema.jsonify(transaction)

#endpoint to delete transaction
@transaction_api.route('/transaction/<id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transactions.query.get(id)
    db.session.delete(transaction)
    db.session.commit()

    return transaction_schema.jsonify(transaction)