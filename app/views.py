import os
from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required, current_app
from app import app, db, lm
from forms import LoginForm, SignupForm, EditProfileForm, PostForm
from models import Post, Follow, User, ROLE_USER, ROLE_ADMIN, db
from werkzeug import secure_filename
######ADDED########################################
from flaskext.mysql import MySQL
import requests
######ADDED########################################
#MySQL configuration.
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'devuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'devpwd'
app.config['MYSQL_DATABASE_DB'] = 'tourini2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['FLASKY_FOLLOWERS_PER_PAGE'] = 20
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/follow/<user_name>')
@login_required
def follow(user_name):
	user = User.query.filter_by(user_name=user_name).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('.user', user_name=user_name))
	current_user.follow(user)
	flash('You are now following %s.' % user_name)
	return redirect(url_for('.user', user_name=user_name))
	
@app.route('/unfollow/<user_name>')
@login_required
def unfollow(user_name):
	user = User.query.filter_by(user_name=user_name).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	if not current_user.is_following(user):
		flash('You are not following this user.')
		return redirect(url_for('.user', user_name=user_name))
	current_user.unfollow(user)
	flash('You have unfollowed %s.' % user_name)
	return redirect(url_for('.user', user_name=user_name))

@app.route('/followers/<user_name>')
def followers(user_name):
	user = User.query.filter_by(user_name=user_name).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(
		page, per_page= current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp}
				for item in pagination.items]
	return render_template('followers.html', user=user, title="Followers of",
							endpoint='.followers', pagination=pagination,
							follows=follows)
	
@app.route('/followed-by/<user_name>')
def followed_by(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)
							
# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
	form = PostForm()
    # Get the name of the uploaded file
	file = request.files['file']
    # Check if the file is one of the allowed types/extensions
	if file and allowed_file(file.filename):
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(file.filename)
		# Move the file form the temporal folder to
		# the upload folder we setup
		file.save(os.path.join(app.config['UPLOAD_FOLDER']+current_user.user_name, filename))
		# Redirect the user to the uploaded_file route, which
		# will basicaly show on the browser the uploaded file
	if  form.validate_on_submit():
		post = Post(body = form.body.data, 
					user_name= current_user.user_name, 
					url = app.config['UPLOAD_FOLDER'] + current_user.user_name + '/'+ filename)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('.index'))
								
'''
		return redirect(url_for('uploaded_file',
                                filename=filename))
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads/',
                               filename)
'''
		   
#Test the connection of MySQL
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
						   password = form.password.data,
						   location = None,
						   name = None,
						   about_me = None)
			db.session.add(newuser)
			db.session.commit()
			
			session['user_name'] = newuser.user_name
			os.makedirs('uploads'+ '/' +newuser.user_name)
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
	user = User.query.filter_by(user_name = user_name).first()
	if user == None:
		flash('User ' + user_name + ' not found.')
		return redirect(url_for('login'))
	return render_template('profile.html',
		user = user)
#####################################	
@app.route('/profile')
@login_required
def profile():
  user = User.query.filter_by( user_name = session['user_name'] ).first()
  if 'user_name' not in session:
    return redirect(url_for('login'))
 
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
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
	user = g.user
	form = PostForm()
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html', title = 'Home', form = form, user = user, posts=posts)

	
	
		
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