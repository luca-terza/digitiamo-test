
import os
import logging

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_migrate import Migrate
from backend.helpers import IPCache
from flask_cors import CORS


db = SQLAlchemy()
ma = Marshmallow()
__api_bp = Blueprint('api', __name__)
api = Api(__api_bp)
r_log = logging.getLogger('digi-test')
r_log.info(f'working in => {os.getcwd()}')
app = Flask(__name__, instance_relative_config=False)
CORS(app)
ip_cache = IPCache(max_size=50)


def down_case_first_letter(s): return s[:1].upper() + s[1:] if s else ''


def create_app(pyenv=None):
    """Initialize the core application."""
    py_env = pyenv or down_case_first_letter(os.getenv("FLASK_ENV"))
    r_log.info(f"config: {py_env}")
    print(f"config: {py_env}")
    app.config.from_object('backend.configuration.' + py_env + "Config")
    # Initialize Plugins
    db.init_app(app)
    Migrate(app, db)

    # importing the models to make sure they are known to Flask-Migrate
    from .models import Call, CallResult
    ma.init_app(app)
    with app.app_context():
        from .dgt_api.v1_0 import digitest_api as rest_api
        api.add_resource(rest_api.CallUrlRes, '/api/v1.0/request_url/<method>')
        app.register_blueprint(__api_bp)
        return app
