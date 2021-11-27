from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import query
from .models import Note,Deck,Card
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST', 'PUT'])
@login_required
def home():
    if request.method == 'POST':
        deck = json.loads(request.data)
        print(deck)
        deckName = deck["deckName"]

        if len(deckName) < 1:
             flash('deckName is too short!', category='error')
        else:
            new_deck = Deck(name=deckName, user_id=current_user.id)
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
            # print(storedDeck)
            # if storedDeck:
            #     query = '''
            #             UPDATE deck
            #             SET
            #             name=?
            #             WHERE id = ?
            #         '''
            #     db.session.execute(query,
            #     [deckName,deckId])
            #     db.session.commit()
        except:
            db.session.rollback()
            flash('Something Went Wrong, Please Try Again', category='error')
    
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

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
            new_card = Card(front=request.form['front'], back=request.form['back'], known=0,type=0,deck_id=request.form['deck_name'])
            db.session.add(new_card)
            db.session.commit()
            flash('Successfully added the card',category='success')
        except:
            db.session.rollback()
            flash('Something Went Wrong, Please Try Again', category='error')
    return render_template("add.html", user=current_user)

