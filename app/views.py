from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, SignupForm
from models import User, ROLE_USER, ROLE_ADMIN, db
######ADDED########################################
from flaskext.mysql import MySQL
import requests
######ADDED########################################

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'devuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'devpwd'
app.config['MYSQL_DATABASE_DB'] = 'tourini'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(user_name = form.user_name.data, 
						   password = form.password.data)
			db.session.add(newuser)
			db.session.commit()
			
			session['user_name'] = newuser.user_name
			flash('User successfully registered')
			return redirect(url_for('login'))
			#return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

#####################################	
@app.route('/profile')
def profile():
 
  if 'user_name' not in session:
    return redirect(url_for('login'))
 
  user = User.query.filter_by( user_name = session['user_name'] ).first()
 
  if user is None:
    return redirect(url_for('login'))
  else:
    return render_template('profile.html')	
#####################################	
'''
#login 
@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['user_name', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/login1', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('index'))
		flash('Invalid username or password.')
	return render_template('login.html', form=form)
'''
'''	
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by( user_name = form.user_name.data ).first()
		user_name = form.user_name.data
		password = form.password.data
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * from user2 where user_name='" + user_name + "' and password='" + password + "';")
		data = cursor.fetchone()
		if data is None:
			flash ("Invalid username or password.")
			return redirect(url_for('login'))
		else:
			flash('You were successfully logged in')
			login_user(user, form.remember_me.data)
			return redirect(url_for('index'))
	return render_template('login.html', form=form)
'''	
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      session['user_name'] = form.user_name.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('login.html', form=form)		



		
#After Login
#@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        user_name = resp.user_name
        if user_name is None or user_name == "":
            user_name = resp.email.split('@')[0]
        user = User(user_name = user_name, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

#	
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
############################################################################
@app.route('/user/<user_name>')
#@login_required
def user(user_name):
    user = User.query.filter_by(user_name = user_name).first()
    if user == None:
        flash('User ' + user_name + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        posts = posts)
	
#	
@app.before_request
def before_request():
    g.user = current_user
		
############################################################################		
@app.route('/')
@app.route('/index')
#@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'user_name': 'John' },
            'body': 'Beautiful day in New York University!'
        },
        {
            'author': { 'user_name': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)
#######################################################		
@app.route('/signout')
def signout():
 
  if 'user_name' not in session:
    return redirect(url_for('login'))
     
  session.pop('user_name', None)
  return redirect(url_for('index'))

@app.route('/about')
def about():
	return render_template('login.html')
	
@app.route('/contact')
def contact():
	return render_template('login.html')	  
'''
@app.route('/logout')
@login_required
def logout():
    logout_user()
	#flash('You have been logged out.')
    return redirect(url_for('index'))
'''