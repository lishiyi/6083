from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, TextAreaField
from wtforms.validators import Required, Email

#from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User

class LoginForm(Form):
	user_name = StringField("User Name",  [validators.Required("Please enter your user name.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	remember_me = BooleanField('Keep me logged in', default = False)
	submit = SubmitField("Log In")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(user_name = self.user_name.data.lower()).first()
		#if user and (user.password == self.password):
		if user is not None and user.check_password(self.password.data):
			return True
		else:
			self.user_name.errors.append("Invalid user name or password")
			return False

class SignupForm(Form):
	user_name = StringField("User name",  [validators.Required("Please enter your user name.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

 
	def validate(self):
		if not Form.validate(self):
			return False
     
		user = User.query.filter_by(user_name = self.user_name.data.lower()).first()
		if user:
			self.user_name.errors.append("That user name is already taken")
			return False
		else:
			return True	
			
class EditProfileForm(Form):
	name = StringField('Real name')
	location = StringField('Location')
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')