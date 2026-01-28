from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Level

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            error = 'Username and password are required.'
        else:
            user = User.query.filter_by(username=username).first()
            
            if user is None:
                error = 'Invalid username or password.'
            elif not check_password_hash(user.password, password):
                error = 'Invalid username or password.'
            else:
                # Enable permanent session so cookie persists for PERMANENT_SESSION_LIFETIME (7 days)
                session.permanent = True
                login_user(user)
                return redirect(url_for('main.dashboard'))
    
    return render_template('login.html', error=error)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password or not confirm_password:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long.'
        elif password != confirm_password:
            error = 'Passwords do not match!'
        elif User.query.filter_by(username=username).first():
            error = 'Username already exists!'
        elif User.query.filter_by(email=email).first():
            error = 'Email already registered!'
        else:
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            
            # Auto-login the new user with persistent session for authentication cookie
            session.permanent = True
            login_user(user)
            return redirect(url_for('main.dashboard'))
    
    return render_template('register.html', error=error)

@main_bp.route('/logout')
@login_required
def logout():
    # Clear session and cookie
    session.permanent = False
    session.clear()
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    levels = Level.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', levels=levels)

@main_bp.route('/game/<int:level_id>')
@login_required
def game(level_id):
    level = Level.query.get_or_404(level_id)
    if level.user_id != current_user.id:
        return 'Unauthorized', 403
    
    return render_template('game.html', level=level)

@main_bp.route('/api/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.json
    # TODO: Implement message processing with LLM
    return jsonify({'response': 'Message received'})
