from app import app

from flask import render_template, url_for
from flask import session, jsonify, redirect

import os

from app import db

from .forms import CompetitionForm, TeamForm, DataEntryForm, ParameterForm

# ------------------------------------------------------------------------------------------------------
# Competition (database)
# ------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return database()
    
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

# ------------------------------------------------------------------------------------------------------
# Teams
# ------------------------------------------------------------------------------------------------------

@app.route('/teams')
def teams():
    
    return render_template('teams.html', my_team=session.get('my-team'), dbname=db.DATABASE)
    
@app.route('/teams/create', methods=['GET', 'POST'])
def teams_create():
    """
    Create a new database (competition) named *dbname*.
    """
    form = TeamForm()
    
    if form.validate_on_submit():
        # Process the form ...
        print('Creating/editing team id="{}"  name="{}"'.format(form.data['teamId'], form.data['name']))
        c = db.get_db()
        r = c.execute('insert into teams (teamId, name) values (?, ?)', (form.data['teamId'], form.data['name']))
        c.commit()
        return redirect(url_for('teams'))
        
    # New database(?)
    return render_template('team_create.html', form=form)

# ------------------------------------------------------------------------------------------------------
# Raw Scores (Data)
# ------------------------------------------------------------------------------------------------------

        
@app.route('/data')
def data():
    c = db.get_db()
    r = c.execute('select * from raw_scores')
    
    form = DataEntryForm()
    form.teamId.choices = [(-1, 'Select team ...')] + [(r['teamId'], ('{} ({})'.format(r['name'], r['teamId'])) if r['name'] else r['teamId']) for r in db.query_db('select teamId, name from teams order by teamId')]
        
    return render_template('data.html', form=form, dbname=session.get('database_name', 'roborank').replace('.db', ''))
    
# ------------------------------------------------------------------------------------------------------
# Ranking & Analytics
# ------------------------------------------------------------------------------------------------------

@app.route('/analyze')
def analyze():
    params = ParameterForm()
    params.zero_balls.default = session.get('params.zero-balls', 0)
    params.autonomous_points.default = session.get('params.autonomous-points', 1)
    params.climb_points.default = session.get('params.climb-points', 1)
    params.spin_col_points.default = session.get('params.spin-rot-points', 1)
    params.spin_rot_points.default = session.get('params.spin-col-points', 1)
    params.process()
    
    return render_template('analyze.html', dbname=db.DATABASE, form=params)
    
# ------------------------------------------------------------------------------------------------------
# About ...
# ------------------------------------------------------------------------------------------------------

@app.route('/about')
def about():
    return render_template('about.html')

    