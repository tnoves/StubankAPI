from flask import Blueprint, request
from app.database import db, ma

user_details_api = Blueprint('user_details_api', __name__)

# Setup UserDetails model from database
class UserDetails(db.Model):
    __tablename__ = 'UserDetails'
    user_details_id = db.Column('ID', db.Integer, primary_key=True)
    firstname = db.Column('FirstName', db.String(100))
    lastname = db.Column('LastName', db.String(100))
    email = db.Column('Email', db.String(100))
    phone = db.Column('PhoneNumber', db.Integer)
    dob = db.Column('DOB', db.Date)

    def __init__(self, firstname, lastname, email, phone, dob):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.dob = dob

# Setup UserDetails schema
class UserDetailsSchema(ma.Schema):
    class Meta:
        fields = ('user_details_id', 'details_id', 'firstname', 'lastname', 'email', 'phone', 'dob')

# Initialise schemas
user_details_schema = UserDetailsSchema()

# endpoint to get a specific users details from id
@user_details_api.route('/user/details/<id>', methods=['GET'])
def get_user_details(id):
    user_details = UserDetails.query.get(id)
    return user_details_schema.jsonify(user_details)

# endpoint to update a specific users details from id
@user_details_api.route('/user/details/<id>', methods=['PUT'])
def update_user_details(id):
    try:
        user_details = UserDetails.query.get(id)
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        phone = request.json['phone']
        dob = request.json['dob']

        user_details.firstname = firstname
        user_details.lastname = lastname
        user_details.email = email
        user_details.phone = phone
        user_details.dob = dob

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()

    return user_details_schema.jsonify(user_details)