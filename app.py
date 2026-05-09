from flask import Flask, render_template, redirect, url_for, session
from flask_cors import CORS
from config import config
from database import db, User
from auth import auth_bp, init_login_manager
from tasks import tasks_bp
from analytics import analytics_bp
from websocket_events import socketio
import os

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins='*')
    init_login_manager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Routes
    @app.route('/')
    def index():
        """Home page"""
        if 'user_id' in session:
            return redirect(url_for('main.dashboard'))
        return redirect(url_for('auth.login'))
    
    # Register main blueprint
    main_bp = __import__('main', fromlist=['main_bp']).main_bp
    app.register_blueprint(main_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
