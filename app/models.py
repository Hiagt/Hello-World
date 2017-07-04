# -*- coding: utf-8 -*-
from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    time = db.Column(db.DateTime)
    filename = db.Column(db.String(120))
    category = db.Column(db.String(120))
    age = db.Column(db.Integer)

    def __init__(self, username, filename, category):
        self.username = username
        self.filename = filename
        self.category = category

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return '<User %r>' % self.username
