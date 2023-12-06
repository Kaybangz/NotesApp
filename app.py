import os
import bcrypt
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import time
from helpers import login_required
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = 'my_secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(10000), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('notes', lazy=True))

    
with app.app_context():
    db.create_all()
 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
@app.route("/index")
@login_required
def index():
    if session['user_id']:
        user = User.query.filter_by(username=session['username']).first()
        notes = Note.query.filter_by(user_id=session['user_id']).order_by(Note.createdAt).all()
        return render_template("index.html", user=user, notes=notes)
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if not username:
            flash('Username cannot be empty', 'error')
            return render_template('register.html')

        if len(password) < 6 or not password:
            flash('Password should be at least 6 characters long', 'error')
            return render_template('register.html')

        if confirmPassword != password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists, choose a different one', 'error')
            return render_template('register.html')

        new_user = User(
            username = username,
            password = password
        )

        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.id

        session['user_id'] = user_id
        session['username'] = username
        session['password'] = password
        
        return redirect('/index')

    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Please enter username', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['password'] = user.password
            return redirect('/index')
        else:
            flash('Login unsuccessful. Invalid user', 'error')
            return render_template('login.html')

    return render_template("login.html")


@app.route("/add_note", methods=["GET", "POST"])
@login_required
def create_new():
    form = NoteForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        user_id = session['user_id']
        
        new_note = Note(
            title = title,
            content = content,
            user_id = user_id
        )

        form.title.data = ''
        form.content.data = ''

        db.session.add(new_note)
        db.session.commit()

        flash('Note added successfully', 'success')
        return redirect('/index')

    return render_template("create_note.html", form=form)
    
@app.route("/note/<int:id>")
@login_required
def view_note(id):

    note = Note.query.get_or_404(id)
    user_id = session['user_id']

    if user_id != note.user_id:
        flash('You are not authorized to view this note.')
        return redirect('/index')

    return render_template("note.html", note=note)

@app.route("/note/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_note(id):

    note = Note.query.get_or_404(id)
    user_id = session['user_id']

    if user_id != note.user_id:
        flash('You are not authorized to update this note.')
        return redirect('/index')

    form = NoteForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content

        db.session.commit()

        flash('Note updated successfully.')
        return render_template("note.html", note=note)

    form.title.data = note.title
    form.content.data = note.content

    return render_template("update.html", form=form, note=note)

@app.route("/note/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_note(id):
    user = User.query.filter_by(username=session['username']).first()
    notes = Note.query.filter_by(user_id=session['user_id']).order_by(Note.createdAt).all()
    
    note = Note.query.get_or_404(id)
    user_id = session['user_id']

    if user_id != note.user_id:
        flash('You are not authorized to delete this note.')
        return redirect('/index')

    try:
        db.session.delete(note)
        db.session.commit()
        flash('Deleted note successfully.')
        notes = Note.query.filter_by(user_id=session['user_id']).order_by(Note.createdAt).all()
        return render_template("index.html", user=user, notes=notes)

    except:
        flash('There was a problem, could not delete note.')

        notes = Note.query.filter_by(user_id=session['user_id']).order_by(Note.createdAt).all()
        return render_template("index.html", user=user, notes=notes)

    return render_template("index.html", user=user, notes=notes)

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)