from datetime import datetime

import bleach
from flask_login import UserMixin
from markdown import markdown
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attributes')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    @staticmethod
    def on_change_body(target, value, old_value, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'blockquote', 'code', 'em', 'i', 'li', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))


db.event.listen(Article.body, 'set', Article.on_change_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    comment_id = db.Column(db.Integer, nullable=True)
    disabled = db.Column(db.Boolean, default=False)

    @staticmethod
    def on_change_body(target, value, old_value, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'blockquote', 'code', 'em', 'i', 'li', 'pre', 'strong', 'ul', 'h1',
                        'h2', 'h3', 'p']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))


db.event.listen(Article.body, 'set', Comment.on_change_body)
