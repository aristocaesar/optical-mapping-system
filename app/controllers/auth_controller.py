from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.users import User
from app.models.sessions import Session
from app.models.session_data import SessionData
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['fullname'] = user.fullname
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Email or password wrong!', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    total_sessions = Session.query.count()
    total_data = SessionData.query.count()
    
    return render_template(
        'dashboard.html', 
        fullname=session.get('fullname', 'User'),
        total_sessions=total_sessions,
        total_data=total_data
    )
