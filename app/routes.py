""" File containing all routes for the project """
from app import app, db, login_manager
from app.forms import RegisterForm, LoginForm
from app.models.user import User
from flask import render_template, redirect, url_for, session
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return user.user_id

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/crm')
def crm():
    return render_template('admin.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.is_submitted():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user:
            print("user doesn't exist")
            return redirect(url_for("login"))
        
        elif not check_password_hash(user.password, password):
            print("wrong password")
            return redirect(url_for("login"))
        
        else:
            session["iduser"] = user.user_id
            load_user(user.user_id)
            return redirect(url_for("crm"))

    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.is_submitted():
        email = form.email.data
        if not form.duplicate_email(email):
            name = form.name.data
            hashed_password = generate_password_hash(form.password.data,
                                                    method="pbkdf2:sha256",
                                                    salt_length=8)
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('crm'))

    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))