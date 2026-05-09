from flask import Blueprint, jsonify, session
from database import db, Task, User
from functools import wraps
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

def login_required_api(f):
    """Decorator for API routes requiring login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@analytics_bp.route('/summary', methods=['GET'])
@login_required_api
def get_analytics_summary():
    """Get analytics summary using Pandas & NumPy"""
    try:
        user_id = session.get('user_id')
        tasks = Task.query.filter_by(user_id=user_id).all()
        
        if not tasks:
            return jsonify({
                'success': True,
                'data': {
                    'total_tasks': 0,
                    'completed_tasks': 0,
                    'pending_tasks': 0,
                    'in_progress_tasks': 0,
                    'cancelled_tasks': 0,
                    'completion_percentage': 0,
                    'pending_percentage': 0,
                    'priority_distribution': {},
                    'status_distribution': {}
                }
            }), 200
        
        # Convert to DataFrame for analysis
        tasks_data = [{
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'priority': task.priority,
            'created_at': task.created_at,
            'completed_at': task.completed_at
        } for task in tasks]
        
        df = pd.DataFrame(tasks_data)
        
        # Calculate statistics
        total_tasks = len(df)
        completed_tasks = len(df[df['status'] == 'completed'])
        pending_tasks = len(df[df['status'] == 'pending'])
        in_progress_tasks = len(df[df['status'] == 'in_progress'])
        cancelled_tasks = len(df[df['status'] == 'cancelled'])
        
        completion_percentage = round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
        pending_percentage = round((pending_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
        
        # Priority distribution
        priority_dist = df['priority'].value_counts().to_dict()
        status_dist = df['status'].value_counts().to_dict()
        
        # Calculate average completion time
        completed_df = df[df['status'] == 'completed']
        if len(completed_df) > 0:
            completion_times = (completed_df['completed_at'] - completed_df['created_at']).dt.total_seconds() / 3600
            avg_completion_time = round(completion_times.mean(), 2)
            max_completion_time = round(completion_times.max(), 2)
            min_completion_time = round(completion_times.min(), 2)
        else:
            avg_completion_time = 0
            max_completion_time = 0
            min_completion_time = 0
        
        # Tasks by week (last 4 weeks)
        today = datetime.utcnow()
        four_weeks_ago = today - timedelta(days=28)
        recent_tasks = df[df['created_at'] >= four_weeks_ago]
        recent_tasks_copy = recent_tasks.copy()
        recent_tasks_copy['week'] = recent_tasks_copy['created_at'].dt.isocalendar().week
        tasks_by_week = recent_tasks_copy['week'].value_counts().sort_index().to_dict()
        
        return jsonify({
            'success': True,
            'data': {
                'total_tasks': int(total_tasks),
                'completed_tasks': int(completed_tasks),
                'pending_tasks': int(pending_tasks),
                'in_progress_tasks': int(in_progress_tasks),
                'cancelled_tasks': int(cancelled_tasks),
                'completion_percentage': completion_percentage,
                'pending_percentage': pending_percentage,
                'avg_completion_time_hours': avg_completion_time,
                'max_completion_time_hours': max_completion_time,
                'min_completion_time_hours': min_completion_time,
                'priority_distribution': priority_dist,
                'status_distribution': status_dist,
                'tasks_by_week': tasks_by_week
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/trends', methods=['GET'])
@login_required_api
def get_trends():
    """Get task trends using NumPy"""
    try:
        user_id = session.get('user_id')
        tasks = Task.query.filter_by(user_id=user_id).all()
        
        if not tasks:
            return jsonify({
                'success': True,
                'data': {
                    'daily_trend': [],
                    'status_velocity': {}
                }
            }), 200
        
        # Convert to DataFrame
        tasks_data = [{
            'created_at': task.created_at.date(),
            'status': task.status
        } for task in tasks]
        
        df = pd.DataFrame(tasks_data)
        
        # Daily trend
        daily_counts = df.groupby('created_at').size().to_dict()
        daily_trend = [
            {'date': str(date), 'count': count}
            for date, count in sorted(daily_counts.items())
        ]
        
        # Status velocity (tasks completed per day)
        completed_tasks = [task for task in tasks if task.status == 'completed']
        if completed_tasks:
            completed_dates = [task.completed_at.date() for task in completed_tasks]
            date_counts = {}
            for date in completed_dates:
                date_counts[date] = date_counts.get(date, 0) + 1
            status_velocity = [
                {'date': str(date), 'completed': count}
                for date, count in sorted(date_counts.items())
            ]
        else:
            status_velocity = []
        
        return jsonify({
            'success': True,
            'data': {
                'daily_trend': daily_trend,
                'status_velocity': status_velocity
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
