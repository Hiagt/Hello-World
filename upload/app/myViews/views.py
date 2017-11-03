# -*- coding: utf-8 -*-
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
from ..models import UserData
from app import db
import json


class MyView(BaseView):

    @expose('/')
    def index(self):
        db_query = db.session.query(UserData).all()
        print db_query
        data = list()
        for f in db_query:
            a = str(f.time)
            f.time = a
            data.append(UserData.to_json(f))
        # return jsonify({'data': data})
        return self.render('test.html')

    @expose('/json')
    def return_json(self):
        db_query = db.session.query(UserData).all()
        print db_query
        data = list()
        for f in db_query:
            a = str(f.time)
            f.time = a
            data.append(UserData.to_json(f))
        print 1
        return jsonify(data)
