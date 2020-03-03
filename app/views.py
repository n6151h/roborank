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
    return render_template('analyze.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/database/create', methods=['GET', 'POST'])
def database_create():
    """
    Create a new database (competition) named *dbname*.
    """
    form = CompetitionForm()
    import pdb; pdb.set_trace()
    
    if form.validate_on_submit():
        # Process the form ...
        db.init_db(form.data['name'])
        return redirect('/database')
        
    # New database(?)
    return render_template('database_create.html', form=form)
        
    
    
@app.route('/database')
def database():
    db_list =  [(c, c.replace('.db', '')) for c in filter(lambda x: x if x.endswith('.db') else None, os.listdir('.'))]
    
    return render_template('database.html', competitions=db_list, current_db=session.get('database_name', ''))

@app.route('/teams')
def teams():
    conn = db.get_db()
    result = conn.execute('select * from teams')
    teams = [(x['teamId'], x['name'] or '(no name)') for x in result.fetchall()]
    return render_template('teams.html', teams=teams)
    
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
    return render_template('data.html')