from app import db
from app.utils.timezone import get_wib_now

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_wib_now)
    updated_at = db.Column(db.DateTime, default=get_wib_now, onupdate=get_wib_now)
    
    # Relationship to SessionData
    data_points = db.relationship('SessionData', backref='session', lazy=True)
