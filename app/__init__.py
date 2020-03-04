"""
RoboRank Main Entrypoint
========================


"""

from flask import Flask, session
from flask_session import Session 

from flask_bootstrap import Bootstrap

app = Flask('roborank', template_folder='app/templates')
app.config.from_pyfile('roborank.cfg')
app.config['SECRET_KEY'] = b'de316fa1fb081ca01d74e7de85b8cd26'

Session(app)
Bootstrap(app)


from app import db

#db.init_db(session.get('database_name', None))

from app import views

from app import api

