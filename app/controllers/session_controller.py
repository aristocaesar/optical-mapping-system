from flask import Blueprint, request, jsonify
from app.models.sessions import Session
from app.models.session_data import SessionData
from app import db
from app.utils.scoring import calculate_piecewise_score

session_bp = Blueprint('session', __name__)

@session_bp.route('/store-session', methods=['POST'])
def store_session():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # Get the active session
    active_session = Session.query.filter_by(is_active=True).first()
    
    if not active_session:
        return jsonify({'error': 'Tidak ada sesi pemetaan yang aktif'}), 400
        
    try:
        # Hitung skor kelayakan lahan menggunakan piecewise linear
        calculated_score = calculate_piecewise_score(data)
        
        new_data = SessionData(
            session_id=active_session.id,
            lat=data.get('lat'),
            lon=data.get('lon'),
            hum=data.get('hum'),
            temp=data.get('temp'),
            ec=data.get('ec'),
            ph=data.get('ph'),
            n=data.get('n'),
            p=data.get('p'),
            k=data.get('k'),
            score=calculated_score
        )
        
        db.session.add(new_data)
        db.session.commit()
        
        return jsonify({
            'message': 'Data successfully saved',
            'session_id': active_session.session_id,
            'data_id': new_data.id,
            'score': calculated_score
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
