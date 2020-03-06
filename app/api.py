from app import app

from flask import render_template, make_response
from flask import request, jsonify
from flask import session

from app import db
import os

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
    
@app.route('/a/scores/add', methods=['POST'])
def add_scores():
    """
    Add rows to raw_scores table.
    """
    import pdb; pdb.set_trace()
    
    return jsonify({'status': 'success'})
    
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
    filtered_scores = db.query_db('select count(*) from raw_scores' + dataTable_request_to_sql(request.values, search_only=True)[0], args)[0]['count(*)']
    
    return jsonify({'teamId': teamId, 
                    'roundId': roundId,
                    'isJson': request.is_json,
                    'status': 'success',
                    'count': len(result),
                    'recordsTotal': total_scores,
                    'recordsFiltered': filtered_scores,
                    'data': result,
                    })
    
@app.route('/a/scores', methods=['POST'])
def create_scores():
    """
    REST endpoint for adding or updating scores.
    """
    if not request.is_json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
        
    # Make sure we have at least some of the requisite data
    teamId = request.json.get('teamId')
    roundId = request.json.get('roundId')
    low_balls = request.json.get('low_balls', 0)
    high_balls = request.json.get('high_balls', 0)
    autonomous = request.json.get('autonomous', False)
    climb = request.json.get('climb', False)
    spin_by_colour = request.json.get('spin_by_colour', False)
    spin_by_rotate = request.json.get('spin_by_rotate', False)
    
    if None in [teamId, roundId]:
        return make_response(jsonify({'error': 'Missing arguments'}), 400)

    qs = """insert or replace into raw_scores(teamId, round, low_balls, high_balls, autonomous, climb, spin_by_colour, spin_by_rotate)
                values (?, ?, ?, ?, ?, ?, ?, ?)"""
    args = [teamId, roundId, low_balls, high_balls, autonomous, climb, spin_by_colour, spin_by_rotate]
    
    result = db.query_db(qs, args)
    
    db.get_db().commit()
    
    return jsonify({
                    'isJson': request.is_json,
                    'status': 'success',
                    'data': {
                        'teamId': teamId, 'roundId': roundId, 
                        'low_balls': low_balls, 'high_balls': high_balls,
                        'climb': climb, 'autonomous': autonomous,
                        'spin_by_colour': spin_by_colour, 'spin_by_rotate': spin_by_rotate
                        }                 
                    })
    
        
@app.route('/a/scoress/<teamId>/roundId/', methods=['DELETE'])
def delete_scores(teamId, roundId):
    """
    REST endpoint to delete a score by teamId and round.
    """
    
    if not request.is_json:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    qs = 'delete from raw_scores where teamId=? and round=?'
    db.query_db(qs, [teamId, roundId])
    db.get_db().commit()
    
    return jsonify({
                    'isJson': request.is_json,
                    'status': 'success',
                    'data': {}
                    })

     
    
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

    session['my-team'] = teamId if teamId != '@@' else ''
    
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
    
    
@app.route('/a/ranking/', methods=['GET'])
def ranking():
    """
    REST endpoint for getting ranking.
    """
    
    # Get the scores.  Exclude teams already selected unless otherwise specified.
    qs = "select * from raw_scores"
    if request.values.get('all_teams', 't') != 't':
        qs += " where teamId in (select teamId from teams where exclude = 'f')"

    # Filter, if specified.        
    if 'search[value]' in request.values and request.values['search[value]']:
        pass  # place-holder for now.

    raw_scores = db.query_db(qs, dict())

    # Get my team ID.
    my_id = db.query_db('select teamId from teams where ')
    #result = [db.row_to_dict(r) for r in db.query_db(qs, args)]
    #filtered_ranking = len(result)
    result = list()

    total_ranking = len(raw_scores)
    filtered_ranking = len(raw_scores)
    
    if 'start' in request.values:
        result = result[int(request.values['start']):]
    if 'length' in request.values:
        result = result[:int(request.values['length'])]    
        
    return jsonify({
                    'isJson': request.is_json,
                    'status': 'success',
                    'count': len(result),
                    'recordsTotal': total_ranking,
                    'recordsFiltered': filtered_ranking,
                    'data': result,
                    })    