"""
Database stuff.

                                             _
(Yes, I cut/pasted this from the flask docu. ¯\_(ツ)_/¯ )
"""

import sqlite3
from flask import g, session
from flask import flash
import sys
import os

from app import app

DATABASE = 'roborank'

def full_db_path(dbname=None):
    if dbname is None:
        dbname = DATABASE
        
    return os.path.join(app.config['COMPETITION_DIR'], dbname + '.db')
    
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
    
def get_db(dbname=None):
    global DATABASE
    
    if dbname is None:
        dbname = DATABASE
        
    DATABASE = dbname
    
    # Does it exist yet?  If not, set a flag to initialize it ... later.
    if not os.path.exists(full_db_path()):
        with app.app_context():
            db = sqlite3.connect(full_db_path())
            with app.open_resource('{}.sql'.format('roborank-template'), mode='r') as f:
                try:
                    db.cursor().executescript(f.read())
                    db.commit()
                    print('Database "{}" created and initialized'.format(dbname))
                except sqlite3.OperationalError as e:
                    if 'already exists' not in e.args[0]:
                        print("Couldn't create database '{0}': {1}".format(dbname, e.args[0]), file=sys.stderr)
                        return

    db = sqlite3.connect(full_db_path())
    db.row_factory = sqlite3.Row

    return db

def row_to_dict(r):
    return dict(zip(r.keys(), r))