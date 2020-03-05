from app import app

from flask import render_template, url_for
from flask import session, jsonify, redirect

import os

from app import db

from .forms import CompetitionForm, TeamForm


@app.route('/')
def index():
    return render_template('main.html')
    
@app.route('/analyze')
def analyze():
    return render_template('analyze.html', dbname=db.DATABASE)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/database/create', methods=['GET', 'POST'])
def database_create():
    """
    Create a new database (competition) named *dbname*.
    """
    form = CompetitionForm()
    
    if form.validate_on_submit():
        # Process the form ...
        
        # Need to save whatever the current dbname is as get_db will change this.
        cur_db = db.DATABASE
        db.get_db(form.data['name'])
        db.get_db(cur_db)  # change it back.
        
        return redirect('/database')
        
    # New database(?)
    return render_template('database_create.html', form=form)
        
    
    
@app.route('/database')
def database():
    db_list =  [(c, c.replace('.db', '')) for c in filter(lambda x: x if x.endswith('.db') else None, os.listdir(os.path.join('.', app.config['COMPETITION_DIR'])))]
    
    if 'database_name' not in session:
        session['database_name'] = db.DATABASE + '.db'
        
    return render_template('database.html', competitions=db_list, current_db=session['database_name'])

@app.route('/teams')
def teams():
    conn = db.get_db()
    result = conn.execute('select * from teams')
    teams = [(x['teamId'], x['name'] or '(no name)') for x in result.fetchall()]
    return render_template('teams.html', teams=teams, my_team=session.get('my-team'), dbname=db.DATABASE)
    
@app.route('/teams/create', methods=['GET', 'POST'])
def teams_create():
    """
    Create a new database (competition) named *dbname*.
    """
    form = TeamForm()
    
    if form.validate_on_submit():
        # Process the form ...
        print('Creating/editing team id="{}"  name="{}"'.format(form.data['id'], form.data['name']))
        c = db.get_db()
        r = c.execute('insert into teams (teamId, name) values (?, ?)', (form.data['id'], form.data['name']))
        c.commit()
        return redirect(url_for('teams'))
        
    # New database(?)
    return render_template('team_create.html', form=form)
        
@app.route('/data')
def data():
    c = db.get_db()
    r = c.execute('select * from raw_scores')
    
    return render_template('data.html', dbname=session.get('database_name', 'roborank').replace('.db', ''))