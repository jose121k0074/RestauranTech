#from flask import current_app as app, render_template
from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')