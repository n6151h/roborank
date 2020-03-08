from app import app

from flask import render_template, make_response
from flask import request, jsonify
from flask import session

from .forms import DataEntryForm, ParameterForm

from app import db
import os

import clu 
import pandas as pd

def dataTable_request_to_sql(rqv, search_only=False):
    """
    Returns a string that can be tacked onto a SQL query
    to narrow the search.
    
    If *search_only* is ``True``, only return as much of the query
    as is needed for filtering -- no ordering or limits.
    
    Returns the string and any arguments required for the search.
    """
    qs = ""
    args = list()
    
    # Ordering
    if 'order[0][column]' in rqv:
        col = rqv['order[0][column]']
        col_name = rqv['columns[{}][name]'.format(col)]
        dir = rqv['order[0][dir]']

    # search filter?    
    if ('search[value]' in rqv) and rqv['search[value]'].strip():
        qs += " where {} like ?".format(col_name)
        args.append(rqv['search[value]'] + '%')
        
    # Just a basic search.
    if search_only:
        return qs, args
        
    # Ordering
    if 'order[0][column]' in rqv:
        qs += ' order by {}'.format(rqv['columns[{}][name]'.format(col)])
        if dir in ['dsc', 'des', 'desc']:
            qs += ' desc'
              
    # Limit?  
    if 'length' in rqv:
        qs += ' LIMIT {}'.format(rqv['length'])
    if 'start' in rqv:
        qs += ' OFFSET {}'.format(rqv['start'])
        
    return qs, args
    
# ------------------------------------------------------------------------------------------------------
# Scores 
# ------------------------------------------------------------------------------------------------------

    
@app.route('/a/scores/<teamId>/<roundId>', methods=['DELETE'])
def delete_scores(teamId, roundId):
    """
    REST endpoint to delete a score by teamId and round.
    """
    
    try:
        dc = db.get_db()
        cur = dc.cursor()
        cur.execute('delete from raw_scores where teamId=? and round=?', [teamId, roundId])
        dc.commit()
        dc.close()
    except Exception as e:
        return jsonify({ 'status': 500, 'message': e.args[0]})
    
    return jsonify({'status': 'success'})
    

@app.route('/a/scores', methods=['POST', 'PUT'])
def add_scores():
    """
    Add rows to raw_scores table.
    """
    
    
    form = DataEntryForm(request.form)
    
    if form.errors:
        return jsonify({'errors': form.errors, 'status': 500})
        
    fields = list(filter(lambda x: x if x != 'csrf_token' else None, form._fields.keys()))
    qs = '''insert into raw_scores ({}) values (?, ?, ?, ?, ?, ?, ?, ?)'''.format(','.join(fields))
    
    try:
        dc = db.get_db()
        cur = dc.cursor()
        cur.execute(qs, [form.data[k] for k in fields])
        dc.commit()
        dc.close()
    except Exception as e:
        return jsonify({ 'status': 500, 'errors': [e.args[0]]})

    return jsonify({'status': 200})
    
@app.route('/a/scores/', methods=['GET'])
def scores(teamId=None, roundId=None):
    """
    REST endpoint for getting raw scores.
    """
    
    qs = 'select * from raw_scores left join teams on raw_scores.teamId = teams.teamId'
    
    xs, args = dataTable_request_to_sql(request.values)
    qs += xs
    
    result = [db.row_to_dict(r) for r in db.query_db(qs, args)]
    total_scores = db.query_db('select count(*) from raw_scores')[0]['count(*)']
    filtered_scores = db.query_db('select count(*) from raw_scores' + \
                                  dataTable_request_to_sql(request.values, search_only=True)[0], args)[0]['count(*)']
    
    return jsonify({'teamId': teamId, 
                    'roundId': roundId,
                    'isJson': request.is_json,
                    'status': 'success',
                    'count': len(result),
                    'recordsTotal': total_scores,
                    'recordsFiltered': filtered_scores,
                    'data': result,
                    })

     
    
# ------------------------------------------------------------------------------------------------------
# Teams
# ------------------------------------------------------------------------------------------------------

@app.route('/a/teams', methods=['GET'])
def teams_get():
    """
    REST endpoint fro getting team info.
    """
    
    xs, args = dataTable_request_to_sql(request.values)
    qs = "select * from teams" + xs
    
    result = [db.row_to_dict(r) for r in db.query_db(qs, args)]

    recordsTotal = db.query_db('select count(*) from teams')[0]['count(*)']
    recordsFiltered = db.query_db('select count(*) from teams' + dataTable_request_to_sql(request.values, search_only=True)[0], args)[0]['count(*)']

    return jsonify({
                    'isJson': request.is_json,
                    'status': 'success',
                    'recordsTotal': recordsTotal,
                    'recordsFiltered': recordsFiltered,
                    'data': result
                    })
   
@app.route('/a/teams/<teamId>/tog-ex', methods=['GET', 'POST'])
def teams_toggle_exclude(teamId):
    """
    Endpoint for deleting a team.
    """

    try:
        dc = db.get_db()
        cur = dc.cursor()
        cur.execute('select * from teams where teamId=?', [int(teamId)])
        team = cur.fetchone()
        cur.execute('update teams set exclude=? where teamId=?', [0 if team['exclude'] != 0 else 1, teamId])
        xx = cur.fetchall()
        dc.commit()
        dc.close()
    except Exception as e:
        return jsonify({ 'status': 'error', 'message': e.args[0]}, code=500)
    
    return jsonify({'status': 'success'})
        
@app.route('/a/teams/<teamId>/my-team', methods=['GET', 'POST'])
def teams_set_my_team(teamId):
    """
    Endpoint for deleting a team.
    """

    session['my-team'] = int(teamId) if teamId != '@@' else ''
    
    return jsonify({'status': 'success', 'my-team': teamId })
        
    
@app.route('/a/teams/<teamId>', methods=['DELETE'])
def teams_delete(teamId):
    """
    Endpoint for deleting a team.
    """

    try:
        dc = db.get_db()
        cur = dc.cursor()
        cur.execute('delete from teams where teamId=?', [int(teamId)])
        dc.commit()
        dc.close()
    except Exception as e:
        return jsonify({ 'status': 'error', 'message': e.args[0]}, code=500)
    
    return jsonify({'status': 'success'})

@app.route('/a/teams', methods=['POST'])
def create_team():
    """
    REST endpoint to create a new team.
    """

    if not request.is_json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
        
    teamId = request.json.get('teamId')
    name = request.json.get('name')
    
    if None in [teamId, name]:
        return make_response(jsonify({'error': 'Missing arguments'}), 400)
    
    qs = 'insert or replace into teams values(?, ?)'
    args = [teamId, name]
    result = db.query_db(qs, args)
    db.get_db().commit()
    
    return jsonify({
                    'isJson': request.is_json,
                    'status': 'success',
                    'data': {
                        'teamId': teamId, 'name': name,                    
                    }})

@app.route('/a/teams/<teamId>', methods=['DELETE'])
def delete_team(teamId):
    """
    REST endpoint to delete a team by ID.
    """
    
    if not request.is_json:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    qs = 'delete from teams where teamId=?'
    db.query_db(qs, [teamId])
    db.get_db().commit()
    
    return jsonify({
                    'isJson': request.is_json,
                    'status': 'success',
                    'data': {}
                    })

# ------------------------------------------------------------------------------------------------------
# Competitions (databases) 
# ------------------------------------------------------------------------------------------------------

@app.route('/a/database/set/<dbName>')
def database_set(dbName):
    """
    Sets working database to *dbName*.
    """
    dbFileName = dbName + '.db'
    
    if not os.path.exists(os.path.join(app.config['COMPETITION_DIR'], dbFileName)):
        raise(ValueError('Databbase "{}" not found.'))
        
    db.get_db(dbName)
    session['database_name'] = dbFileName 

    return jsonify({'status': 'success', 'current_db': dbFileName})
    
    
# ------------------------------------------------------------------------------------------------------
# Ranking & Analytics
# ------------------------------------------------------------------------------------------------------

@app.route('/a/ranking', methods=['GET'])
def ranking():
    """
    Return ranked pairs of teams of *team_size*.   
    
    Teams that have been excluded (see Teams page) will not be included in these
    calculations.
    
    Note: one of the teams must be desginated as "my team" (see Teams page)
    for any ranking to be calculated.
    """
    
    # Make sure my-team is set.  Error if not.
    if session['my-team'] is None or session['my-team'] == '@@':
        return jsonify({'status': 500, 'errors': ["My Team not set."]})
        
    # Get the raw scores for all non-excluded teams.
    raw_data = [db.row_to_dict(r) for r in db.query_db("select * from raw_scores left join teams on raw_scores.teamId = teams.teamId where teams.exclude=0")]
    
    # Split into rounds
    rounds = clu.split_into_rounds(raw_data, round_col='round')
    
    # Calculate scores
    raw_scores = list()
    
    point_vals = {
        'autonomous': session.get('params.autonomous-points', 1), 
        'climb':  session.get('params.climb-points', 1),
        'spin_by_colour':  session.get('params.spin-by-col-points', 1),
        'spin_by_rotate':  session.get('params.spin-by-rot-points', 1)
    }
    
    for rnd in rounds.values():
        try:
            rnd_scores = clu.calc_scores_for_round(rnd, 
                                                us_id=session['my-team'], 
                                                id_col='teamId',
                                                point_values=None, 
                                                zero_balls=session.get('params.zero-balls', 0),
                                                balls_low_col='low_balls', 
                                                balls_high_col='high_balls',
                                                auto_col='autonomous', 
                                                climb_col='climb', 
                                                spin_clr_col='spin_by_colour',
                                                spin_rot_col='spin_by_rotate', 
                                                round_col='round')
            raw_scores.extend(rnd_scores)
        except ValueError:  # My team not in this round -- ignore for now.
            print("My team ({}) is not in this round ({})".format(session['my-team'], rnd[0]['round']))
            pass
    
    # Aggregate scores
    ag_scores = pd.DataFrame(clu.aggregate_scores(raw_scores), columns=['pair', 'score', 'std_dev', 'adj_score'])
    total = len(ag_scores)

    rqv = request.values   # saves me some typing.
    
    #import pdb; pdb.set_trace()
    # Ordering
    if 'order[0][column]' in rqv:
        col = rqv['order[0][column]']
        col_name = rqv['columns[{}][name]'.format(col)]
        asc = rqv['order[0][dir]'] not in ['dsc', 'des', 'desc']
        ag_scores = ag_scores.sort_values(by=[col_name], ascending=asc)
    
    # Filter ...
    if ('search[value]' in rqv) and rqv['search[value]'].strip():
        sv = rqv['search[value]'].strip()
        ag_scores = ag_scores[[sv in str(x) for x in ag_scores['pair'].to_list()]]

    filtered = len(ag_scores)
    
    # Any searching / filtering?
    if 'start' in rqv:
        ag_scores = ag_scores[int(rqv['start']):]
    if 'length' in rqv:
        ag_scores = ag_scores[:int(rqv['length'])]
    
    return jsonify({'status': 200,
                    'data': ag_scores.to_dict(orient='records'),
                    'rounds': len(rounds),
                    "recordsTotal": total,
                    "recordsFiltered": filtered,
                   })
    
    
@app.route('/a/ranking/params', methods=['POST'])
def ranking_params():
    """
    Set parameters used by ranking algorithm.
    """
    params = ParameterForm(request.form)
    
    if not params.validate():
        return jsonify({'status': 500, 'message': "Invalid parameter(s)"})
        
    session['params.zero-balls'] = params.zero_balls.data
    session['params.autonomous-points'] = params.autonomous_points.data
    session['params.climb-points'] = params.autonomous_points.data
    session['params.spin-col-points'] = params.spin_col_points.data
    session['params.spin-rot-points'] = params.spin_rot_points.data

    return jsonify({'status': 200})