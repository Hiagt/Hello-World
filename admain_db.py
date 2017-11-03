from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    # def to_json(self):
    #     return dict(
    #         id=self.id,
    #         username=self.username,
    #         password=self.password,
    #         email=self.email
    #     )


# class Commodity(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     commodity_name = db.Column(db.String(100), unique=True)
#     commodity_price = db.Column(db.String(100), unique=True)
#
#     def __init__(self, commodity_name, commodity_price):
#         self.commodity_name = commodity_name
#         self.commodity_price = commodity_price
#
#     def __repr__(self):
#         return '<User %r>' % self.commodity_name
#
#     def to_json(self):
#         return dict(
#             id=self.id,
#             commodity_name=self.commodity_name,
#             commodity_price=self.commodity_price,
#         )
