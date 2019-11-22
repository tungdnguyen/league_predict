from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class TeamForm(FlaskForm):
	player1=StringField('Player 1', validators=[DataRequired()])
	champ1=StringField('Champion 1', validators=[DataRequired()])
	player2=StringField('Player 2', validators=[DataRequired()])
	champ2=StringField('Champion 2', validators=[DataRequired()])
	player3=StringField('Player 3', validators=[DataRequired()])
	champ3=StringField('Champion 3', validators=[DataRequired()])
	player4=StringField('Player 4', validators=[DataRequired()])
	champ4=StringField('Champion 4', validators=[DataRequired()])
	player5=StringField('Player 5', validators=[DataRequired()])
	champ5=StringField('Champion 5', validators=[DataRequired()])
	
	submit=SubmitField('Predict')