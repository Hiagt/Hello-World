# -*- coding: utf-8 -*-
import os.path as op
from flask import Flask, Session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from config import config

BASE_DIR = op.dirname(__file__)     # 做dir拼接
FILE_DIR = list()
db = SQLAlchemy()
admin = Admin()
babel = Babel()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    file_dir = config['development'].UPLOAD_FOLDER  # 后面加判断做地址拼接
    FILE_DIR.append(file_dir)

    db.init_app(app)
    admin.init_app(app)
    babel.init_app(app)
    # sess.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    # 通过引用模型生成后台管理页面
    from .models import User, UserData
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(UserData, db.session))
    from .myViews import views
    admin.add_view(views.MyView(name='ajax', endpoint='ajax'))

    return app
