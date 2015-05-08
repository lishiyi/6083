from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
#from hashlib import md5
#import hashlib

ROLE_USER = 0
ROLE_ADMIN = 1

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_name = db.Column(db.String(45))
	url = db.Column(db.String(45))


class Follow(db.Model):
	__tablename__ = 'follows2'
	follower_id = db.Column(db.Integer, db.ForeignKey('user2.user_id'),
	primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('user2.user_id'),
	primary_key=True)
	timestamp = db.Column(db.DateTime, default = datetime.utcnow)

class User(db.Model):
	
	__tablename__ = 'user2'
	user_id = db.Column(db.Integer, primary_key = True)
	user_name = db.Column(db.String(45), unique=True)
	password = db.Column(db.String(45))
	location = db.Column(db.String(45))
	name = db.Column(db.String(45))
	about_me = db.Column(db.Text())
	
	followed = db.relationship('Follow',
								foreign_keys=[Follow.follower_id],
								backref=db.backref('follower', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	followers = db.relationship('Follow',
								foreign_keys=[Follow.followed_id],
								backref=db.backref('followed', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	
	def __init__(self, user_name, password, location, name, about_me):
		
		self.user_name = user_name.title()
		self.password = password.title()
		if location:
			self.location = location.title()
		if name:
			self.name = name.title()
		if about_me:
			self.about_me = about_me.title()
	
	def check_password(self, password):
		return password == self.password
	
		
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.user_id)

	def __repr__(self):
		return '<User %r>' % (self.user_name)
		
	def follow(self, user):
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)
			
	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.user_id).first()
		if f:
			db.session.delete(f)
			
	def is_following(self, user):
		return self.followed.filter_by(
			followed_id = user.use_id).first() is not None
	def is_followed_by(self, user):
		return self.followers.filter_by(
			follower_id = user.user_id).first() is not None