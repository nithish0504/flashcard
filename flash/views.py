from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import query
from .models import Deck,Card
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST', 'PUT'])
@login_required
def home():
    if request.method == 'POST':
        deck = json.loads(request.data)
      
        deckName = deck["deckName"]

        if len(deckName) < 1:
             flash('deckName is too short!', category='error')
        else:
            new_deck = Deck(name=deckName,type=0,score=0, user_id=current_user.id)
            db.session.add(new_deck)
            db.session.commit()
            flash('Deck added!', category='success')
    elif request.method == 'PUT':
        try:
            deck = json.loads(request.data)
            deckName=deck["deckName"]
            deckId = deck["deckId"]
            Deck.query.filter_by(id=deckId).update(dict(name=deckName))
            db.session.commit()
            flash('Deck saved', category='success')
          
        except:
            db.session.rollback()
            flash('Something Went Wrong, Please Try Again', category='error')
    
    return render_template("home.html", user=current_user)




@views.route('/delete-deck', methods=['POST'])
def delete_deck():
    got_deck = json.loads(request.data)
    deckId = got_deck['deckId']

    try:
        deck = Deck.query.get(deckId)
        if deck:
            if deck.user_id == current_user.id:
                db.session.delete(deck)
                db.session.commit()
                flash('Deck deleted successfully!', category='success')
    except:
        db.session.rollback()
        flash('Something Went Wrong, Please Try Again', category='error')

    return jsonify({})

@views.route('/add_card', methods=['GET', 'POST'])
@login_required
def home1():
    if request.method=='POST':
        try:
            new_card = Card(front=request.form['front'], back=request.form['back'], known=0, visited=0, type=0,deck_id=request.form['deck_name'])
            db.session.add(new_card)
            db.session.commit()
            flash('Successfully added the card',category='success')
        except:
            db.session.rollback()
            flash('Something Went Wrong, Please Try Again', category='error')
    return render_template("add.html", user=current_user)

@views.route('/cards/<deckId>', methods=['GET', 'POST'])
@login_required
def cards(deckId):
    if request.method=='GET':
        # try:
            __card=None
        
            cards= Card.query.filter_by(deck_id=deckId).all()
            for _card in cards:
               
                if _card.visited==0:
                    __card=_card
                    break

            if __card == None:
                __card="deck finished"
            #db.session.commit()
         
            return render_template("card.html",card=__card,user=current_user)
        # except :
        #     #db.session.rollback()
        #     flash('Something Went Wrong, Please Try Again', category='error')
   # return render_template("add.html", user=current_user)

@views.route('/card/edit/<cardId>', methods=['GET', 'POST'])
@login_required
def cards_edit(cardId):
    if request.method=='POST':
        try:
           
            Card.query.filter_by(id=cardId).update(dict(front=request.form['front'], back=request.form['back']))
            db.session.commit()
            flash('Successfully edited the card',category='success')
        except:
            db.session.rollback()
            flash('Something Went Wrong, Please Try Again', category='error')
        return render_template("add.html", user=current_user)
    elif request.method=='GET':
        card=Card.query.filter_by(id=cardId).first()
        return render_template('edit.html',card=card,user=current_user)

@views.route('/delete-card', methods=['POST'])
def delete_card():
    got_deck = json.loads(request.data)
    cardId = got_deck['cardId']

    try:
        card = Deck.query.get(cardId)
        if card:
                db.session.delete(card)
                db.session.commit()
                flash('card deleted successfully!', category='success')
    except:
        db.session.rollback()
        flash('Something Went Wrong, Please Try Again', category='error')

    return jsonify({})

@views.route('/update-score/<cardId>', methods=['GET', 'POST'])
@login_required
def update_score(cardId):
    
    if request.method =='POST':

       
            _card=Card.query.filter_by(id=cardId).first()
            deckId=_card.deck_id
            Card.query.filter_by(id=cardId).update(dict(visited=1))
            level=request.form["score"]
            deck = Deck.query.filter_by(id=deckId).first()
            _score=deck.score+int(level)
            Deck.query.filter_by(id=deckId).update(dict(score=_score))
            db.session.commit()
            flash('Score Updated', category='success')

            __card = None
            cards= Card.query.filter_by(deck_id=deckId).all()
            for _card1 in cards:
                
                if _card1.visited==0:
                    __card=_card1
                    break

            if __card == None:
                __card="deck finished"
        
            return render_template("card.html",card=__card,user=current_user)
     
        
    
