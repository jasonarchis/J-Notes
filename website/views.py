from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Note
from datetime import datetime
import json


views = Blueprint('views', __name__)


# Landing page before logging in.
@views.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.userhome'))
    return render_template('index.html', user=current_user)


# User home page onced logged in.
# Handles creating and saving notes.
@views.route('/user-home/', methods=['GET', 'POST'])
@login_required
def userhome():
    if request.method == 'POST':      
        note = request.form
        n_title = note['title']
        n_content = note['content']
        n_id = note['note_id']
        
        # note or title too short
        if len(n_content) < 1:
            flash('Note is too short!', category="error")
        elif len(n_title) <1:
            flash('Title is too short!', category="error")
        else:
            # check form button id to see if user has pressed save
            if 'sb_save' in request.form:
                note = Note.query.filter_by(note_id=n_id).first()
                if note:
                    note.title = n_title
                    note.content = n_content
                    note.date = datetime.now()
                    db.session.commit()
                    flash('Note saved!')
                else:
                    flash('You must create a note before saving it!', category="error")
            # otherwise user has chosen to add new note
            else:
                n_dtime = datetime.now()
                new_note = Note(content=n_content, title=n_title, user_id=current_user.id, date=n_dtime)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!')

    return render_template('userhome.html', user=current_user)


# User delete note.
@views.route('/delete-note', methods=["POST"])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})
