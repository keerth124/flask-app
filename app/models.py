from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, json, app
from app import app, db, login, ma



followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class UserLogins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    login_date = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    logins = db.relationship('UserLogins', backref='loginauthor', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), index=True)
    brand = db.Column(db.String(256), index=True)
    wtype = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256))
    size = db.Column(db.String(64))
    price = db.Column(db.String(64))
    link = db.Column(db.String(256))
    store = db.Column(db.String(128), index=True)
    quantity = db.Column(db.String(128))
    address = db.Column(db.String(256), index=True)
    phone = db.Column(db.String(64))
    insertTime = db.Column(db.DateTime, index=True)


    def __repr__(self):
        return '<Inventory {}>'.format(self.id)

class DataHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datadatetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sku = db.Column(db.String(64), index=True)
    wtype = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256))
    size = db.Column(db.String(64))
    price = db.Column(db.String(64))
    store = db.Column(db.String(128), index=True)
    quantity = db.Column(db.String(128))
    address = db.Column(db.String(256), index=True) 

    def __repr__(self):
        return '<DataHistory {}>'.format(self.id)

class LastUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recordcount = db.Column(db.Integer)
    datestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completionTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return '<LastUpdate {}>'.format(self.id)

class InventorySchema(ma.ModelSchema):
    class Meta:
        model = Inventory
        sqla_session = db.session

''' example
inventory = Inventory(sku='22395', brand='Deutsch Family WIne and Spirits',wtype='Bourbon / Ryle Whisky',description='Redemption Rye',size='.75L',price='$25.95',link='/products/locations?ID=46',store='Store #47',quantity='47 Bottles',address='1426-B South Tryon St.',phone='9194135014')
    username='susan', email='susan@example.com')

'''