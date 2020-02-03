"""
RoboRank Main Entrypoint
========================


"""

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = b'de316fa1fb081ca01d74e7de85b8cd26'

import db

db.init_db()

import api

Bootstrap(app)

from flask import render_template

@app.route('/')
def index():
    return render_template('main.html')
    
@app.route('/analyze')
def analyze():
    return render_template('a.html')
    
@app.route('/about')
def about():
    return render_template('about.html')
    
