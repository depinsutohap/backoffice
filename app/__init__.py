from sanic import Sanic
from sanic_session import Session as _Session
from sanic_mail import Sanic_Mail
from sanic_jinja2 import SanicJinja2
from sanic_auth import Auth, User
from sanic_cors import CORS, cross_origin
from pymongo import MongoClient
from sanic_jwt import Initialize as init_jwt
from config import config

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool


# db = SQLAlchemy()
# mongo = PyMongo()
# csrf = CSRFProtect()

app = Sanic(__name__)
jinja = SanicJinja2()
_auth = Auth(app)
# engine = create_engine('mysql://hop_bo:!2345hopbo0005432!@178.128.93.105:3306/uta_hop_db_000', echo_pool=True)
engine = create_engine('mysql://hop_bo:!2345HopBo0005432!@157.230.46.218:3306/uta_hop_dev_db_000', poolclass=NullPool)
Base = declarative_base()
Session = sessionmaker(bind=engine)
# sm=Sanic_Mail()

client = MongoClient("mongodb://hop_bo:!2345hopbo0005432!@157.230.46.218:27017/uta_mongo_hop_dev_db_000")
mongo = client.uta_mongo_hop_dev_db_000

def create_app(config_name):
    app.config.from_object(config[config_name])
    app.static('/static', 'app/static')

    CORS(app, resources={r"/api-v1/*": {"origins": "*"}})
    # CORS(app)

    config[config_name].init_app(app)
    _Session(app)
    # sm.init_app(app)
    Session.configure(bind=engine)
    jinja.init_app(app, pkg_path='templates')

    # Create database

    from .main import main as main_blueprint
    app.blueprint(main_blueprint)

    #create blueprint
    from .api_1 import api_1 as api_1_blueprint
    app.blueprint(api_1_blueprint)

    return app
