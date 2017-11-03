# -*- coding: utf-8 -*-
from . import main
from flask import request


@main.route('/')
def index():
    print request.args
    return 'SUCCESS'
