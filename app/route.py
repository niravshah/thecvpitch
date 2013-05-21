import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flask.ext.mongoengine import MongoEngine
 
USERNAME = 'admin'
PASSWORD = 'default'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

app.config['MONGODB_SETTINGS'] = {'DB':'thecvpitch'}
db = MongoEngine(app)

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
 		if request.form['username'] != app.config['USERNAME']:
 			error = 'Invalid username'
 		elif request.form['password'] != app.config['PASSWORD']:
 			error = 'Invalid password'
 		else:
 			session['logged_in'] = True
 			flash('You were logged in')
 			return redirect(url_for('home'))	 	
 	return render_template('login.html', error=error)


@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('home'))


@app.route('/', methods=['GET','POST'])
def home():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		return render_template('index.html')


 
if __name__ == '__main__':
  app.run(debug=True, host = '0.0.0.0')
