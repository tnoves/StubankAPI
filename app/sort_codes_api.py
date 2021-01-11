from flask import Blueprint, request, jsonify
from app.database import db, ma
from app.user_api import UsersSchema

sort_codes_api = Blueprint('sort_codes_api', __name__)

# Setup SortCodes model from database
class SortCodes(db.Model):
    __tablename__ = 'SortCodes'
    sort_code_id = db.Column('SortCodeID', db.Integer, primary_key=True)
    sort_code = db.Column('SortCode', db.String(100))

    def __init__(self, sort_code):
        self.sort_code = sort_code

# Setup SortCodes schema
class SortCodesSchema(ma.Schema):
    class Meta:
        fields = ('sort_code_id', 'sort_code')

# Initialise schemas
sort_codes_schema = SortCodesSchema()

# endpoint to get a specific sort code from id
@sort_codes_api.route('/sort_code/<id>', methods=['GET'])
def get_sort_code(id):
    sort_code = SortCodes.query.get(id)
    return sort_codes_schema.jsonify(sort_code)

# endpoint to update a specific sort code from id
@sort_codes_api.route('/sort_code/<id>', methods=['PUT'])
def update_sort_code(id):
    sort_code = SortCodes.query.get(id)
    sort_code_number = request.json['sort_code']

    sort_code.sort_code = sort_code_number

    db.session.commit()
    return sort_codes_schema.jsonify(sort_code)

#endpoint to delete sort code
@sort_codes_api.route('/sort_code/<id>', methods=['DELETE'])
def delete_sort_code(id):
    sort_code = SortCodes.query.get(id)
    db.session.delete(sort_code)
    db.session.commit()

    return sort_codes_schema.jsonify(sort_code)