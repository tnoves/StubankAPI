import random
import string

from flask import Blueprint, request, jsonify
from sqlalchemy import null

from app.database import db, ma

from app.user_details_api import UserDetails, UserDetailsSchema
from app.account_api import Accounts

user_api = Blueprint('user_api', __name__)

# Setup Users model from database
class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column('UserID', db.Integer, primary_key=True)
    username = db.Column('Username', db.String(100), unique=True)
    password = db.Column('Password', db.String(100))
    user_details_id = db.Column('UserDetailsID', db.Integer)
    account_id = db.Column('AccountID', db.Integer)

    def __init__(self, username, password, user_details_id, account_id):
        self.username = username
        self.password = password
        self.user_details_id = user_details_id
        self.account_id = account_id

# Setup Users schema
class UsersSchema(ma.Schema):
    user_details = ma.Nested(UserDetailsSchema)
    class Meta:
        additional = ('id', 'username', 'password', 'user_details_id', 'account_id')

# Initialise schemas
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

# endpoint to create a user
@user_api.route('/user/', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    dob = request.json['dob']
    email = request.json['email']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    phone = request.json['phone']

    try:
        # Create account for user along with unique random account number
        while True:
            account_number = ''.join(random.choices(string.digits, k=8))
            sort_code_id = 4

            account = Accounts(account_number=account_number, sort_code_id=sort_code_id)
            db.session.add(account)
            db.session.commit()
            if (account.account_id != null):
                break

        account_id = account.account_id

        user_details = UserDetails(dob=dob, email=email, firstname=firstname, lastname=lastname, phone=phone)
        db.session.add(user_details)
        db.session.commit()

        user = Users(username=username, password=password, user_details_id=user_details.user_details_id,
                     account_id=account_id)

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return user_schema.jsonify(user)

# endpoint to get a specific user from id
@user_api.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)

@user_api.route('/user/username/<username>', methods=['GET'])
def get_user_username(username):
    user = Users.query.filter(Users.username == username).first()
    result = user_schema.dump(user)
    return jsonify(result)

@user_api.route('/user/from/details/<user_details>', methods=['GET'])
def get_user_details_id(user_details):
    user = Users.query.filter(Users.user_details_id == user_details).first()
    result = user_schema.dump(user)
    return jsonify(result)

# endpoint to get all users
@user_api.route('/user/all', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

# endpoint to update a specific user from id
@user_api.route('/user/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = Users.query.get(id)
        print (request.json['username'])
        username = request.json['username']

        user.username = username

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return user_schema.jsonify(user)

#endpoint to delete user
@user_api.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)