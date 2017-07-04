# -*- coding: utf-8 -*-
from .. import db
from ..models import User
from .import api, make_json_resp


@api.route('/')
def index():
    user = User.query.filter_by(username='hiagt').first()
    if user:
        pass

    data = {
        'name': 'Hiagt',
        'age': 23
    }
    return make_json_resp(data=data)
