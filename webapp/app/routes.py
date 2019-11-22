#routes.py
from flask import render_template, flash, redirect
from app import app
from app.forms import TeamForm

@app.route('/')
@app.route('/index')

def index():
	return "Hello world"
	
@app.route('/predict', methods=['GET','POST'])
def predict():
	form=TeamForm()
	players=[form.player1.data, form.player2.data, form.player3.data, form.player4.data, form.player5.data]
	champs=[form.champ1.data, form.champ2.data, form.champ3.data, form.champ4.data, form.champ5.data]
	pch=[(players[i],champs[i])for i in range(len(players))]
	if form.validate_on_submit():
		flash('input is {}'.format(pch))
		return redirect('/predict') #send input to model as list of tuples
	return render_template('team.html', form=form)
	
	