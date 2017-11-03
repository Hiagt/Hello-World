# -*- coding: utf-8 -*-
import os
import read_db_dir
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024  # 上传文件大小限制
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_POOL_RECYCLE = 20  # 自动回连
    FLASKY_SLOW_DB_QUERY_TIME = 0.5


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = read_db_dir.get_upload_dir()  # 上传地址
    DOWNLOAD_FOLDER = read_db_dir.get_upload_dir()  # 下载地址
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #     'mysql+pymysql://root:root@localhost:3306/test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              read_db_dir.sql_dir()

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
