from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import time
from app.models.sessions import Session
from app.models.session_data import SessionData
from app import db

from app.utils.timezone import get_wib_now

web_session_bp = Blueprint('web_session', __name__)

@web_session_bp.before_request
def check_auth():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

@web_session_bp.route('/sessions')
def sessions_page():
    return render_template('sessions.html')

@web_session_bp.route('/sessions/data', methods=['POST'])
def sessions_data():
    draw = request.form.get('draw', type=int)
    start = request.form.get('start', type=int)
    length = request.form.get('length', type=int)
    order_column_index = request.form.get('order[0][column]', type=int)
    order_dir = request.form.get('order[0][dir]', 'asc')
    search_value = request.form.get('search[value]', '')
    
    columns = ['id', 'session_id', 'name', 'is_active', 'created_at']
    order_column = columns[order_column_index] if order_column_index < len(columns) else 'created_at'
    
    query = Session.query
    
    if search_value:
        query = query.filter(
            Session.session_id.ilike(f'%{search_value}%') |
            Session.name.ilike(f'%{search_value}%')
        )
        
    total_filtered = query.count()
    
    if order_dir == 'asc':
        query = query.order_by(db.asc(getattr(Session, order_column)))
    else:
        query = query.order_by(db.desc(getattr(Session, order_column)))
        
    query = query.offset(start).limit(length)
    
    data = []
    for s in query.all():
        data.append({
            'id': s.id,
            'session_id': s.session_id,
            'name': s.name,
            'is_active': s.is_active,
            'created_at': s.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
        
    return jsonify({
        'draw': draw,
        'recordsTotal': Session.query.count(),
        'recordsFiltered': total_filtered,
        'data': data
    })

@web_session_bp.route('/sessions/store', methods=['POST'])
def store_session():
    name = request.form.get('name')
    is_active = request.form.get('is_active') == 'true'
    
    # Generate session_id using epoch time
    session_id = f"OCM-{int(time.time())}"
        
    if is_active:
        Session.query.update({Session.is_active: False})
        
    new_session = Session(
        session_id=session_id, 
        name=name, 
        is_active=is_active,
        created_at=get_wib_now(),
        updated_at=get_wib_now()
    )
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Session added successfully.'})

@web_session_bp.route('/sessions/update/<int:id>', methods=['POST'])
def update_session(id):
    s = Session.query.get_or_404(id)
    
    name = request.form.get('name')
    is_active = request.form.get('is_active') == 'true'
        
    if is_active and not s.is_active:
        Session.query.update({Session.is_active: False})
        
    s.name = name
    s.is_active = is_active
    s.updated_at = get_wib_now()
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Session updated successfully.'})

@web_session_bp.route('/sessions/delete/<int:id>', methods=['POST'])
def delete_session(id):
    s = Session.query.get_or_404(id)
    SessionData.query.filter_by(session_id=id).delete()
    db.session.delete(s)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Session deleted successfully.'})

@web_session_bp.route('/sessions/detail/data/delete/<int:id>', methods=['POST'])
def delete_session_data(id):
    d = SessionData.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Data deleted successfully.'})

@web_session_bp.route('/sessions/detail/data/update_coords/<int:id>', methods=['POST'])
def detail_update_coords(id):
    d = SessionData.query.get_or_404(id)
    lat = request.form.get('lat', type=float)
    lon = request.form.get('lon', type=float)
    
    if lat is not None and lon is not None:
        d.lat = lat
        d.lon = lon
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Coordinates updated successfully.'})
    
    return jsonify({'status': 'error', 'message': 'Invalid data.'}), 400

@web_session_bp.route('/sessions/detail/<int:id>')
def detail_page(id):
    session_obj = Session.query.get_or_404(id)
    
    total_data = SessionData.query.filter_by(session_id=id).count()
    total_baik = SessionData.query.filter(SessionData.session_id == id, SessionData.score >= 75).count()
    total_cukup = SessionData.query.filter(SessionData.session_id == id, SessionData.score >= 50, SessionData.score < 75).count()
    total_buruk = SessionData.query.filter(SessionData.session_id == id, SessionData.score < 50).count()
    
    # Get first data point for initial map view
    first_point = SessionData.query.filter_by(session_id=id).order_by(SessionData.id.asc()).first()
    default_lat = first_point.lat if first_point else -8.219233
    default_lon = first_point.lon if first_point else 114.369227
    
    return render_template('session_detail.html', 
                           mapping_session=session_obj,
                           total_data=total_data,
                           total_baik=total_baik,
                           total_cukup=total_cukup,
                           total_buruk=total_buruk,
                           default_lat=default_lat,
                           default_lon=default_lon)

@web_session_bp.route('/sessions/detail/<int:id>/map_data')
def detail_map_data(id):
    # Dapatkan data secara berurutan berdasar ID (untuk menghubungkan jalur dengan benar)
    data_points = SessionData.query.filter_by(session_id=id).order_by(SessionData.id.asc()).all()
    
    result = []
    for d in data_points:
        category = "Poor"
        if d.score >= 75:
            category = "Good"
        elif d.score >= 50:
            category = "Moderate"
            
        result.append({
            'id': d.id,
            'lat': d.lat,
            'lon': d.lon,
            'score': d.score,
            'category': category,
            'created_at': d.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return jsonify(result)

@web_session_bp.route('/sessions/detail/<int:id>/table_data', methods=['POST'])
def detail_table_data(id):
    search_value = request.form.get('search[value]', '')
    order_column_index = request.form.get('order[0][column]', type=int)
    order_dir = request.form.get('order[0][dir]', 'asc')
    draw = request.form.get('draw', type=int)
    start = request.form.get('start', type=int)
    length = request.form.get('length', type=int)
    
    # Map column index to model attributes
    columns = ['id', 'created_at', 'lat', 'lon', 'ph', 'hum', 'temp', 'ec', 'n', 'p', 'k', 'score']
    order_column = columns[order_column_index] if order_column_index < len(columns) else 'id'
    
    query = SessionData.query.filter_by(session_id=id)
    
    if search_value:
        # Simple search for score or coordinates if they match exactly as strings
        query = query.filter(
            db.cast(SessionData.id, db.String).ilike(f'%{search_value}%') |
            db.cast(SessionData.score, db.String).ilike(f'%{search_value}%')
        )
    
    total_filtered = query.count()
    
    if order_dir == 'asc':
        query = query.order_by(db.asc(getattr(SessionData, order_column)))
    else:
        query = query.order_by(db.desc(getattr(SessionData, order_column)))
        
    query = query.offset(start).limit(length)
    
    data = []
    for d in query.all():
        category = "Poor"
        if d.score >= 75:
            category = "Good"
        elif d.score >= 50:
            category = "Moderate"
            
        data.append({
            'id': d.id,
            'lat': d.lat,
            'lon': d.lon,
            'hum': d.hum,
            'temp': d.temp,
            'ec': d.ec,
            'ph': d.ph,
            'n': d.n,
            'p': d.p,
            'k': d.k,
            'score': d.score,
            'category': category,
            'created_at': d.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return jsonify({
        'draw': draw,
        'recordsTotal': SessionData.query.filter_by(session_id=id).count(),
        'recordsFiltered': total_filtered,
        'data': data
    })

@web_session_bp.route('/sessions/detail/<int:id>/all_data')
def detail_all_data(id):
    query = SessionData.query.filter_by(session_id=id).order_by(SessionData.id.asc()).all()
    data = []
    for d in query:
        category = "Poor"
        if d.score >= 75: category = "Good"
        elif d.score >= 50: category = "Moderate"
        data.append({
            'id': d.id,
            'lat': d.lat,
            'lon': d.lon,
            'hum': d.hum,
            'temp': d.temp,
            'ec': d.ec,
            'ph': d.ph,
            'n': d.n,
            'p': d.p,
            'k': d.k,
            'score': d.score,
            'category': category,
            'created_at': d.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(data)
