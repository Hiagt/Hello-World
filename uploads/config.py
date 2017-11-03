# -*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 基础配置
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECRET_KEY = '123'  # os.environ.get('SECRET_KEY') or
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024       # 上传文件大小限制
    UPLOAD_FOLDER = r"C:\Users\wz\Desktop\uploads\app\static\uploads"       # 上传地址
    DOWNLOAD_FOLDER = r"C:\Users\wz\Desktop\uploads\app\static\downloads"       # 下载地址

    @staticmethod
    def init_app(app):
        pass


# 每个配置类继承基础类，方便配置更改调用
class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}
