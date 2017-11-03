from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commodity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commodity_name = db.Column(db.String(100), unique=True)
    commodity_price = db.Column(db.String(100), unique=True)

    def __init__(self, commodity_name, commodity_price):
        self.commodity_name = commodity_name
        self.commodity_price = commodity_price

    def __repr__(self):
        return '<User %r>' % self.commodity_name

    # def to_json(self):
    #     return dict(
    #         id=self.id,
    #         commodity_name=self.commodity_name,
    #         commodity_price=self.commodity_price,
    #     )
