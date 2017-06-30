# -*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 基础配置
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECRET_KEY = 'hard to guess string'  # os.environ.get('SECRET_KEY') or
    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
