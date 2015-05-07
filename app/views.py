from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, SignupForm, EditProfileForm
from models import User, ROLE_USER, ROLE_ADMIN, db
######ADDED########################################
from flaskext.mysql import MySQL
import requests
######ADDED########################################

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'devuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'devpwd'
app.config['MYSQL_DATABASE_DB'] = 'tourini2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

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

	elif request.method == 'GET':
		return render_template('signup.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if request.method == 'POST':
		if form.validate() == False:
			flash ("Invalid username or password.")
			return render_template('login.html', form=form)
		else:
			session['user_name'] = form.user_name.data
			user = User.query.filter_by( user_name = form.user_name.data).first()
			login_user(user)
			flash('You were successfully logged in')
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('login.html', form=form)		
		
#After Login
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

####################################################	
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
############################################################################
@app.route('/user/<user_name>')
@login_required
def user(user_name):
    #user = User.query.filter_by(user_name = user_name).first()
	user = g.user
	if user == None:
		flash('User ' + user_name + ' not found.')
		return redirect(url_for('login'))

	return render_template('profile.html',
		user = user)
#####################################	
@app.route('/profile')
@login_required
def profile():
  user = g.user
  if 'user_name' not in session:
    return redirect(url_for('login'))
 
  #user = User.query.filter_by( user_name = session['user_name'] ).first()
 
  if user is None:
    flash('User ' + user_name + ' not found.')
    return redirect(url_for('login'))

  else:
    return render_template('profile.html',
		user = user)	
		
@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		g.user.name = form.name.data
		g.user.location = form.location.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your profile has been updated.')
		return redirect(url_for('.user', user_name= g.user.user_name))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)
		
#####################################	
###############################	
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
            'author': { 'user_name': 'Lina' },
            'body': 'Beautiful day in New York University!'
        },
        {
            'author': { 'user_name': 'Kimi' },
            'body': 'The Great Wall is so cool!'
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
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('index'))

@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/contact')
def contact():
	return render_template('contact.html')	  