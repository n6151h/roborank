from app import app

from flask import render_template, make_response
from flask import request, jsonify
from flask import session

from app import db
import os

@app.route('/a/scores/', methods=['GET'])
@app.route('/a/scores/<teamId>', methods=['GET'])
@app.route('/a/scores/<teamId>/<roundId>', methods=['GET'])
def scores(teamId=None, roundId=None):
    """
    REST endpoint for getting raw scores.
    """
    
    qs = 'select * from raw_scores'
    args = list()
    
    if teamId is not None:
        qs += " where teamId=?"
        args.append(teamId)
    if roundId is not None:
        qs += ' and round=?'
        args.append(roundId)
        
    if 'search[value]' in request.values and request.values['search[value]']:
        if "where" not in qs:
            qs += " where"
        else:
            qs += " and"
        qs += " teamId like ?"
        args.append(request.values['search[value]'] + '%')
        
    total_scores = db.query_db('select count(*) from raw_scores')[0]['count(*)']
    
    result = [db.row_to_dict(r) for r in db.query_db(qs, args)]
    filtered_scores = len(result)
    
    if 'start' in request.values:
        result = result[int(request.values['start']):]
    if 'length' in request.values:
        result = result[:int(request.values['length'])]    
        
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
                    'count': 1,
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

     
    
@app.route('/a/teams/', methods=['GET'])
@app.route('/a/teams/<teamId>', methods=['GET'])
def teams_get(teamId=None, methods=['GET']):
    """
    REST endpoint fro getting team info.
    """
    
    qs = "select * from teams"
    args = list()
    
    if teamId is not None:
        qs += ' where teamId=?'
        args.append(teamId)
        
    result = db.query_db(qs, args)
    return jsonify({'teamId': teamId, 
                    'isJson': request.is_json,
                    'status': 'success',
                    'count': len(result),
                    'data': {
                        'teams': [ db.row_to_dict(r) for r in result]
                    }})
   
    
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
        
    session['database_name'] = dbFileName 

    return jsonify({'status': 'success', 'current_db': dbFileName})
    