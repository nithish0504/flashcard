from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class Deck(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.String(40))
    score = db.Column(db.Integer)
    review_time = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

class Card(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    front = db.Column(db.String(40))
    back = db.Column(db.String(40))
    known = db.Column(db.Integer)
    visited=db.Column(db.Integer)
    type = db.Column(db.Integer)
    deck_id=db.Column(db.Integer,db.ForeignKey('deck.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
 
    decks=db.relationship('Deck')
