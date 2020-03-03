from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import DataRequired

class CompetitionForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class TeamForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    name = StringField('name', validators=[])
    