import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flask.ext.mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
 
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
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Document):
	username = db.StringField(max_length=60)
    	password = db.StringField()
	role = db.StringField()	
	active = db.BooleanField()
	def is_active(self):
		return self.active
	def get_id(self):
		return self.username
	def is_authenticated(self):
		return True
	def is_anonymous(self):
		return False

@login_manager.user_loader
def load_user(id):
    return User.objects(username=id)[0]



@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		user = User.objects(username=request.form['username'])
		if user.count() > 0:
 			if  request.form['password'] == user[0].password:
				if login_user(user[0]):
					return userhome(current_user)
			else:
				error = 'Invalid Login'
 		else:
 			error = 'Invalid Login'
 	return render_template('login.html', error=error)


@app.route('/logout', methods=['GET','POST'])
def logout():
	logout_user()
	return redirect(url_for('home'))


def userhome(user):
	return  render_template('index.html',user=user)


@app.route('/', methods=['GET','POST'])
@login_required
def home():
	return userhome(current_user)

@login_manager.unauthorized_handler
def unauthorized():
	error = 'login required'
	return render_template('login.html', error=error)

@app.route('/datareset')
@login_required
def data():
	User.objects().delete()
	User(username='admin',password='default',role='admin',active=True).save()
	User(username='nirav',password='nirav', role='jobseeker',active=True).save()
	User(username='curator',password='curator', role='curator',active=True).save()
	User(username='poster',password='poster', role='poster',active=True).save()
 	return 'Data Entered!'

@app.route('/list')
@login_required
def list():
	users = User.objects.all()
	for user in users:
		print user.username
		print user.is_active()
	return'Listed'



if __name__ == '__main__':
  app.run(debug=True, host = '0.0.0.0')
