from app import db
from app.utils.timezone import get_wib_now

class SessionData(db.Model):
    __tablename__ = 'session_data'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    hum = db.Column(db.Float, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    ec = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    n = db.Column(db.Integer, nullable=False)
    p = db.Column(db.Integer, nullable=False)
    k = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=get_wib_now)
