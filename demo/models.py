from .extensions import db


class Stock(db.Model):
    name = db.Column(db.String(10), primary_key=True)
    date = db.Column(db.DateTime(), nullable=True)
    open_price = db.Column(db.Float(), nullable=True)
    close_price = db.Column(db.Float(), nullable=True)
    adjopen_price = db.Column(db.Float(), nullable=True)
    adjclose_price = db.Column(db.Float(), nullable=True)
