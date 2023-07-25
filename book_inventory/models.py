from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    libro = db.relationship('Book', backref='owner', lazy=True)

    def __init__(self, email, username, password, first_name='', last_name=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f'User {self.email} has been added to the database!'
    
class Book(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    cover = db.Column(db.String(150))
    genre = db.Column(db.String(150))
    release_date = db.Column(db.String(150), nullable=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, title, author, cover, genre, release_date, user_token):
        self.id = self.set_id()
        self.title = title
        self.author = author
        self.cover = cover
        self.genre = genre
        self.release_date = release_date
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'{self.title} has been added to the database!'
    

class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'author', 'cover', 'genre', 'release_date']

book_schema = BookSchema()
books_schema = BookSchema(many=True)