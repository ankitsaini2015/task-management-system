from flask import Blueprint, render_template, session, redirect, url_for
from database import Task, User
from functools import wraps

main_bp = Blueprint('main', __name__)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Get task counts
    total_tasks = Task.query.filter_by(user_id=user_id).count()
    completed_tasks = Task.query.filter_by(user_id=user_id, status='completed').count()
    pending_tasks = Task.query.filter_by(user_id=user_id, status='pending').count()
    
    completion_percentage = round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
    
    return render_template('dashboard.html',
                          username=username,
                          total_tasks=total_tasks,
                          completed_tasks=completed_tasks,
                          pending_tasks=pending_tasks,
                          completion_percentage=completion_percentage)

@main_bp.route('/tasks')
@login_required
def tasks():
    """Tasks page"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    return render_template('tasks.html', username=username)
