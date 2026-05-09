from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session
from database import db, Task
import json

socketio = SocketIO(cors_allowed_origins='*')

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    user_id = session.get('user_id')
    if user_id:
        join_room(f'user_{user_id}')
        emit('connection_response', {
            'data': 'Connected to task updates',
            'user_id': user_id
        })
        print(f'User {user_id} connected to WebSocket')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    user_id = session.get('user_id')
    if user_id:
        leave_room(f'user_{user_id}')
        print(f'User {user_id} disconnected from WebSocket')

@socketio.on('task_created')
def handle_task_created(data):
    """Broadcast task creation to user"""
    user_id = session.get('user_id')
    if user_id:
        emit('task_update', {
            'action': 'created',
            'task': data,
            'timestamp': str(__import__('datetime').datetime.utcnow())
        }, room=f'user_{user_id}')

@socketio.on('task_updated')
def handle_task_updated(data):
    """Broadcast task update to user"""
    user_id = session.get('user_id')
    if user_id:
        emit('task_update', {
            'action': 'updated',
            'task': data,
            'timestamp': str(__import__('datetime').datetime.utcnow())
        }, room=f'user_{user_id}')

@socketio.on('task_deleted')
def handle_task_deleted(data):
    """Broadcast task deletion to user"""
    user_id = session.get('user_id')
    if user_id:
        emit('task_update', {
            'action': 'deleted',
            'task_id': data.get('task_id'),
            'timestamp': str(__import__('datetime').datetime.utcnow())
        }, room=f'user_{user_id}')

@socketio.on('get_notifications')
def handle_get_notifications():
    """Send real-time notifications"""
    user_id = session.get('user_id')
    if user_id:
        # Get pending tasks count
        pending_count = Task.query.filter_by(user_id=user_id, status='pending').count()
        # Get overdue tasks (if due_date exists)
        from datetime import datetime
        overdue_count = Task.query.filter(
            Task.user_id == user_id,
            Task.status != 'completed',
            Task.due_date < datetime.utcnow()
        ).count()
        
        emit('notifications', {
            'pending_tasks': pending_count,
            'overdue_tasks': overdue_count
        })

@socketio.on('analytics_request')
def handle_analytics_request():
    """Send analytics data in real-time"""
    user_id = session.get('user_id')
    if user_id:
        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        completed = len([t for t in tasks if t.status == 'completed'])
        pending = len([t for t in tasks if t.status == 'pending'])
        
        emit('analytics_update', {
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': pending,
            'completion_percentage': round((completed / total * 100), 2) if total > 0 else 0
        })
