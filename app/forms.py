from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from wtforms.validators import ValidationError, StopValidation

from app import db
from flask import session
from app import app

import os

class CompetitionForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='Please provide a unique compeition name')])
    
    def validate_name(form, field):
        if os.path.exists(os.path.join(app.config['COMPETITION_DIR'], field.data + '.db')):
            raise StopValidation('Compeition named "{}" already exists. Please choose another name.'.format(field.data))

class TeamForm(FlaskForm):
    teamId = IntegerField('Team ID', validators=[DataRequired()])
    name = StringField('Team Name (optional)')
    
    def validate_id(form, field):
        """ 
        Make sure teamId specified is unique.
        """
        if db.query_db('select count(*) from teams where teamId=?', [field.data])[0]['count(*)'] > 0:
            raise StopValidation('Team "{}" already exists.  Please specify a unique team name.'.format(field.data))
    
class DataEntryForm(FlaskForm):
    round = IntegerField('Round', validators=[InputRequired(message='Round must be a positive integer.'), NumberRange(min=1, max=20)])
    teamId = SelectField('Team ID', validators=[DataRequired()])
    high_balls = IntegerField('High Balls', validators=[NumberRange(min=0)])
    low_balls= IntegerField('Low Balls', validators=[NumberRange(min=0)])
    autonomous = BooleanField('Autonomous')
    climb = BooleanField('Climbing')
    spin_by_colour = BooleanField('Spin (Colour)')
    spin_by_rotate = BooleanField('Spin (Rotate)')
    
    def validate_teamId(form, field):
        """
        Make sure teamId already exists in *teames* table.        
        """
        if field.data == -1:
            raise StopValidation('Please select a team from the Team ID drop-down.')
            
        if db.query_db('select count(*) from teams where teamId=?', [field.data])[0] <= 0:
            raise StopValidation('Team "{}" has not yet been defined.'.format(field.data))
            
            
class ParameterForm(FlaskForm):
    """
    The ranking algorithm has several parameters that can be modified from their defaults to
    alter the resulting ranks.  For example, high or low ball scores that are zero can (and probably should) be
    penalized, so we can apply a handicap (``zero-balls``) to those values.
    """
    zero_balls = IntegerField('Zero-Balls', validators=[NumberRange(min=0, message="Must be non-negative integer." )])
    autonomous_points = IntegerField('Autonomous Value', validators=[NumberRange(min=1, message='Must be > 0')])
    climb_points = IntegerField('Climb Value', validators=[NumberRange(min=1, message='Must be > 0')])
    spin_rot_points = IntegerField('Spin-by-Rotation Value', validators=[NumberRange(min=1, message='Must be > 0')])
    spin_col_points = IntegerField('Spin-by-Colour Value', validators=[NumberRange(min=1, message='Must be > 0')])
        
            
        
            