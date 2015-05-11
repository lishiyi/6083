from app import db, app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import bleach
from markdown import markdown
import flask.ext.whooshalchemy as whooshalchemy

db = SQLAlchemy()
#from hashlib import md5
#import hashlib

ROLE_USER = 0
ROLE_ADMIN = 1

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	disabled = db.Column(db.Boolean)
	author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	######
	
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
						'strong']
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, strip=True))

	def to_json(self):
		json_comment = {
			'url': url_for('api.get_comment', id=self.id, _external=True),
			'post': url_for('api.get_post', id=self.post_id, _external=True),
			'body': self.body,
			'body_html': self.body_html,
			'timestamp': self.timestamp,
			'author': url_for('api.get_user', id=self.author_id,
							  _external=True),
		}
		return json_comment

	@staticmethod
	def from_json(json_comment):
		body = json_comment.get('body')
		if body is None or body == '':
			raise ValidationError('comment does not have a body')
		return Comment(body=body)
		
db.event.listen(Comment.body, 'set', Comment.on_changed_body)


class Post(db.Model):
	__searchable__ = ['body']
	
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_name = db.Column(db.String(45))
	url = db.Column(db.String(45))
	###
	body_html = db.Column(db.Text)
	author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	
	comments = db.relationship('Comment', backref='post', lazy='dynamic')
	
	##############
	@staticmethod
	def generate_fake(count=100):
		from random import seed, randint
		import forgery_py

		seed()
		user_count = User.query.count()
		for i in range(count):
			u = User.query.offset(randint(0, user_count - 1)).first()
			p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
					 timestamp=forgery_py.date.date(True),
					 author=u)
			db.session.add(p)
			db.session.commit()
	
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
						'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
						'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify( bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, strip=True))
			
	def to_json(self):
		json_post = {
			'url': url_for('api.get_post', id=self.id, _external=True),
			'body': self.body,
			'body_html': self.body_html,
			'timestamp': self.timestamp,
			'author': url_for('api.get_user', id=self.author_id,
							  _external=True),
			'comments': url_for('api.get_post_comments', id=self.id,
							    _external=True),
			'comment_count': self.comments.count()
		}
		return json_post

	@staticmethod
	def from_json(json_post):
		body = json_post.get('body')
		if body is None or body == '':
			raise ValidationError('post does not have a body')
		return Post(body=body)
	
	def __repr__(self):
		return '<Post %r>' % (self.body)

whooshalchemy.whoosh_index(app, Post)

db.event.listen(Post.body, 'set', Post.on_changed_body)

class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
	primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
	primary_key=True)
	timestamp = db.Column(db.DateTime, default = datetime.utcnow)

class User(db.Model):
	
	__tablename__ = 'user'
	user_id = db.Column(db.Integer, primary_key = True)
	user_name = db.Column(db.String(45), unique=True)
	password = db.Column(db.String(45))
	location = db.Column(db.String(45))
	name = db.Column(db.String(45))
	about_me = db.Column(db.Text())
	###
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	
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
	###
	comments = db.relationship('Comment', backref='author', lazy='dynamic')
	
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
			db.session.commit()
			
	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.user_id).first()
		if f:
			db.session.delete(f)
			db.session.commit()
			
	def is_following(self, user):
		return self.followed.filter_by(
			followed_id = user.user_id).first() is not None
	def is_followed_by(self, user):
		return self.followers.filter_by(
			follower_id = user.user_id).first() is not None
			
	@property
	def followed_posts(self):
		return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
				.filter(Follow.follower_id == self.user_id)
