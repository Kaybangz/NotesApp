import os
import bcrypt
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_ckeditor import CKEditor
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired
from datetime import datetime
import time
from helpers import login_required

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
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

@app.route("/")
@app.route("/index")
@login_required
def index():
    if session['username']:
        user = User.query.filter_by(username=session['username']).first()
        return render_template("index.html", user=user)
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # Validation 1: Check if username is not empty
        if not username:
            flash('Username cannot be empty', 'error')
            return render_template('register.html')

        # Validation 2: Check password length and non-emptiness
        if len(password) < 6 or not password:
            flash('Password should be at least 6 characters long', 'error')
            return render_template('register.html')

        # Validation 3: Check if confirmPassword matches password
        if confirmPassword != password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        # Validation 4: Check if username already exists in the database
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

        # Validation 1: Check if username is not empty
        if not username:
            flash('Please enter username', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            # Successful login, redirect to a secure page
            session['username'] = user.username
            session['password'] = user.password
            return redirect('/index')
        else:
            flash('Login unsuccessful. Invalid user', 'error')
            return render_template('login.html')

    return render_template("login.html")

@app.route("/create_new", methods=["GET", "POST"])
def create_new():
    return render_template("create_note.html")

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