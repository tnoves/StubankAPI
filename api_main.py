from app.user_api import user_api
from app.card_api import card_api
from app.transaction_api import transaction_api
from app.payment_accounts_api import payment_accounts_api
from app.user_details_api import user_details_api
from app.account_api import account_api
from app.sort_codes_api import sort_codes_api

from app.database import db, ma
import flask
import os
import sshtunnel

app = flask.Flask(__name__)
app.config["DEBUG"] = True
basedir = os.path.abspath(os.path.dirname(__file__))

with open("app/login_details.txt", "r") as file:
    login_info = file.readline().split()

tunnel = sshtunnel.SSHTunnelForwarder(
    ('linux.cs.ncl.ac.uk', 22),
    ssh_username=login_info[0],
    ssh_password=login_info[1],
    remote_bind_address=('cs-db.ncl.ac.uk', 3306)
)

tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://t2033t46:Fox6BuckSeem@127.0.0.1:{}/t2033t46".format(tunnel.local_bind_port)
db.init_app(app)
ma.init_app(app)

app.register_blueprint(user_api)
app.register_blueprint(user_details_api)
app.register_blueprint(card_api)
app.register_blueprint(account_api)
app.register_blueprint(sort_codes_api)
app.register_blueprint(transaction_api)
app.register_blueprint(payment_accounts_api)

@app.route('/home', methods=['GET'])
def home():
    return (str(db.engine.table_names()))

app.run()

