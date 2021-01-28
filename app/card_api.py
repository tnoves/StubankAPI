import random
import string

from flask import Blueprint, request, jsonify
from sqlalchemy import null

from app.database import db, ma
from app.user_api import UsersSchema
from app.account_api import AccountsSchema

card_api = Blueprint('card_api', __name__)

# Setup Cards model from database
class Cards(db.Model):
    __tablename__ = 'Cards'
    card_number = db.Column('16DigitCardNo', db.String(100), primary_key=True)
    account_id = db.Column('AccountID', db.Integer)
    active = db.Column('Active', db.Integer)
    balance = db.Column('Balance', db.Float)
    cvc_code = db.Column('CVC Code', db.Integer)
    card_type = db.Column('CardType', db.String(100))
    expiry_date = db.Column('Expiry Date', db.Date)
    payment_processor = db.Column('PaymentProcessor', db.String(100))
    user_id = db.Column('UserID', db.Integer)

    def __init__(self, card_number, account_id, active, balance, cvc_code, card_type,
                 expiry_date, payment_processor, user_id):
        self.card_number = card_number
        self.account_id = account_id
        self.active = active
        self.balance = balance
        self.cvc_code = cvc_code
        self.card_type = card_type
        self.expiry_date = expiry_date
        self.payment_processor = payment_processor
        self.user_id = user_id

# Setup Cards schema
class CardsSchema(ma.Schema):
    account = ma.Nested(AccountsSchema)
    user = ma.Nested(UsersSchema)
    class Meta:
        additional = ('card_number', 'account_id', 'active', 'balance', 'cvc_code', 'card_type', 'expiry_date',
                      'payment_processor', 'user_id')

# Initialise schemas
card_schema = CardsSchema()
cards_schema = CardsSchema(many=True)

# endpoint to create a card
@card_api.route('/card/', methods=['POST'])
def create_card():
    account_id = request.json['account_id']
    active = request.json['active']
    balance = request.json['balance']
    cvc_code = request.json['cvc_code']
    card_type = request.json['card_type']
    expiry_date = request.json['expiry_date']
    payment_processor = request.json['payment_processor']
    user_id = request.json['user_id']

    # Create card for user along with unique random card number
    while True:
        try:
            card_number = ''.join(random.choices(string.digits, k=16))

            card = Cards(card_number=card_number, account_id=account_id, active=active, balance=balance, cvc_code=cvc_code,
                         card_type=card_type, expiry_date=expiry_date, payment_processor=payment_processor, user_id=user_id)
            db.session.add(card)
            db.session.commit()

            if (card.card_number != null):
                break
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            continue

    return card_schema.jsonify(card)

# endpoint to get a specific card from id
@card_api.route('/card/<id>', methods=['GET'])
def get_card(id):
    card = Cards.query.get(id)
    return card_schema.jsonify(card)

# endpoint to get all cards for a specific user
@card_api.route('/card/user/<id>', methods=['GET'])
def get_all_cards(id):
    cards = Cards.query.filter(Cards.user_id == id).all()
    result = cards_schema.dump(cards)
    return jsonify(result)

# endpoint to update a specific card from id
@card_api.route('/card/<id>', methods=['PUT'])
def update_card(id):
    try:
        card = Cards.query.get(id)
        active = request.json['active']
        balance = request.json['balance']

        card.active = active
        card.balance = balance

        db.session.commit()
    except Exception as e:
        print (e)
        db.session.rollback()
        db.session.flush()

    return card_schema.jsonify(card)

#endpoint to delete card
@card_api.route('/card/<id>', methods=['DELETE'])
def delete_card(id):
    try:
        card = Cards.query.get(id)
        db.session.delete(card)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return card_schema.jsonify(card)