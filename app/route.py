import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flask.ext.mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension

 
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

app.config['MONGODB_SETTINGS'] = {'DB':'thecvpitch'}

app.debug = True
app.config['DEBUG_TB_PANELS'] = (
    'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel',
    'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
    'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
    'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
    'flask.ext.mongoengine.panels.MongoDebugPanel'
)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


db = MongoEngine()
db.init_app(app)

toolbar = DebugToolbarExtension(app)

class User(db.Document):
	username = db.StringField(max_length=60)
    	password = db.StringField()
	role = db.StringField()


@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		user = User.objects(username=request.form['username'])
		if user.count() > 0:
 			if  request.form['password'] == user[0].password:
 				session['logged_in'] = True
 				#return redirect(url_for('home'))	 	
				return home(user)
			else:
				error = 'Invalid Login'
 		else:
 			error = 'Invalid Login'
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


@app.route('/datareset')
def data():
	User.objects().delete()
	User(username='admin',password='default',role='admin').save()
	User(username='nirav',password='nirav', role='jobseeker').save()
 	return 'Data Entered!'

@app.route('/list')
def list():
	users = User.objects.all()
	for user in users:
		print user.username;
	return'Listed'



if __name__ == '__main__':
  app.run(debug=True, host = '0.0.0.0')
