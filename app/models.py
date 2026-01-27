from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    levels = db.relationship('Level', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_number = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Level {self.level_number} for User {self.user_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
