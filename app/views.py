from app import app

from flask import render_template
from flask import session, jsonify, redirect

import os

from app import db


@app.route('/')
def index():
    return render_template('main.html')
    
@app.route('/analyze')
def analyze():
    return render_template('analyze.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/database/create/<dbname>')
def database_create(dbname=None):
    """
    Create a new database (competition) named *dbname*.
    """
    if dbname is None:
        return render_template('database_create.html')
        
    # Process the form ...
    db.init_db(dbname)
    return redirect('/database')
    
@app.route('/database')
def database():
    db_list =  [(c, c.replace('.db', '')) for c in filter(lambda x: x if x.endswith('.db') else None, os.listdir('.'))]
    
    return render_template('database.html', competitions=db_list, current_db=session.get('database_name', ''))

@app.route('/teams')
def teams():
    return render_template('teams.html')
    
@app.route('/data')
def data():
    return render_template('data.html')