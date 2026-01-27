from flask import Blueprint, render_template, request, redirect, url_for, jsonify
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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return 'User already exists!'
        
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/logout')
@login_required
def logout():
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
