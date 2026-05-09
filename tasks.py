from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database import db, Task, User
from datetime import datetime
from functools import wraps
import json

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

def login_required_api(f):
    """Decorator for API routes requiring login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@tasks_bp.route('', methods=['GET'])
@login_required_api
def get_tasks():
    """Get all tasks for the current user"""
    try:
        user_id = session.get('user_id')
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = Task.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        
        tasks = query.order_by(Task.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/<task_id>', methods=['GET'])
@login_required_api
def get_task(task_id):
    """Get a specific task"""
    try:
        user_id = session.get('user_id')
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'data': task.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('', methods=['POST'])
@login_required_api
def add_task():
    """Add a new task"""
    try:
        user_id = session.get('user_id')
        data = request.get_json() or request.form
        
        # Validation
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        if len(title) > 200:
            return jsonify({'success': False, 'error': 'Title must be less than 200 characters'}), 400
        
        priority = data.get('priority', 'medium')
        if priority not in Task.PRIORITY_CHOICES:
            return jsonify({'success': False, 'error': f'Invalid priority. Choose from: {Task.PRIORITY_CHOICES}'}), 400
        
        # Create task
        task = Task(
            user_id=user_id,
            title=title,
            description=data.get('description', ''),
            priority=priority,
            status='pending'
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task added successfully',
            'data': task.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/<task_id>', methods=['PUT'])
@login_required_api
def update_task(task_id):
    """Update a task"""
    try:
        user_id = session.get('user_id')
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        data = request.get_json() or request.form
        
        # Update fields
        if 'title' in data:
            title = data.get('title', '').strip()
            if not title:
                return jsonify({'success': False, 'error': 'Title cannot be empty'}), 400
            task.title = title
        
        if 'description' in data:
            task.description = data.get('description', '')
        
        if 'priority' in data:
            priority = data.get('priority')
            if priority not in Task.PRIORITY_CHOICES:
                return jsonify({'success': False, 'error': f'Invalid priority. Choose from: {Task.PRIORITY_CHOICES}'}), 400
            task.priority = priority
        
        if 'status' in data:
            status = data.get('status')
            if status not in Task.STATUS_CHOICES:
                return jsonify({'success': False, 'error': f'Invalid status. Choose from: {Task.STATUS_CHOICES}'}), 400
            task.status = status
            
            # Set completed_at if task is marked as completed
            if status == 'completed':
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': task.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/<task_id>', methods=['DELETE'])
@login_required_api
def delete_task(task_id):
    """Delete a task"""
    try:
        user_id = session.get('user_id')
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
