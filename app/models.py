# -*- coding: utf-8 -*-
from . import db


class UserData(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    time = db.Column(db.DateTime)
    filename = db.Column(db.String(120))
    category = db.Column(db.String(120))

    def __init__(self, username=None, filename=None, category=None, time=None):
        self.username = username
        self.filename = filename
        self.category = category
        self.time = time

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return '<User %r>' % self.username

    def to_json(self):
        return dict(
            username=self.username,
            filename=self.filename,
            time=self.time,
            category=self.category
        )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username