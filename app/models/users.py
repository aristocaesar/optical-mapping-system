from app import db
from app.utils.timezone import get_wib_now

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=get_wib_now)
    updated_at = db.Column(db.DateTime, default=get_wib_now, onupdate=get_wib_now)
