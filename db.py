"""
Database stuff.

                                             _
(Yes, I cut/pasted this from the flask docu. ¯\_(ツ)_/¯ )
"""

import sqlite3
from flask import g
from flask import flash
import sys
import os

from main import app

DATABASE = 'roborank'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE + '.db')
    db.row_factory = sqlite3.Row        
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    
def init_db(dbname=DATABASE):
    if os.path.exists('{}.db'.format(dbname)):
        print('Using existing database "{}.db"'.format(dbname))
        
    DATABASE = dbname
    with app.app_context():
        db = get_db()
        with app.open_resource('{}.sql'.format(dbname), mode='r') as f:
            try:
                db.cursor().executescript(f.read())
                print('Database "{}" created'.format(dbname))
            except sqlite3.OperationalError as e:
                if 'already exists' not in e.args[0]:
                    print("Couldn't create database '{0}': {1}".format(dbname, e.args[0]), file=sys.stderr)
                    #flash("Couldn't create {0} database: {1}".format(dbname, e.args[0]), 'error')
                return
            
        db.commit()
        #flash('Database "{}" created'.format(dbname))

def row_to_dict(r):
    return dict(zip(r.keys(), r))