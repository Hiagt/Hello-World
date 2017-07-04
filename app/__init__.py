# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from config import config

db = SQLAlchemy()
admin = Admin()
babel = Babel()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    admin.init_app(app)
    babel.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    from .models import User
    admin.add_view(ModelView(User, db.session))

    return app
