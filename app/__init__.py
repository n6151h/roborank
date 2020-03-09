"""
RoboRank Main Entrypoint
========================


"""

from flask import Flask, session
from flask_session import Session 

from flask_bootstrap import Bootstrap

app = Flask('roborank', template_folder='app/templates')
app.config.from_pyfile('roborank.cfg')

Session(app)
Bootstrap(app)


from app import db

from app import views

from app import api

