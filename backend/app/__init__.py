from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.student.routes import student_bp
    from app.lecturer.routes import lecturer_bp
    from app.resources.routes import resources_bp
    
    # Register API blueprints
    from app.auth.api import auth_api_bp
    from app.student.api import student_api_bp
    from app.lecturer.api import lecturer_api_bp
    from app.resources.api import resources_api_bp
    
    # Register HTML routes (for web interface)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    
    # Register API routes
    app.register_blueprint(auth_api_bp, url_prefix='/api/auth')
    app.register_blueprint(student_api_bp, url_prefix='/api/student')
    app.register_blueprint(lecturer_api_bp, url_prefix='/api/lecturer')
    app.register_blueprint(resources_api_bp, url_prefix='/api/resources')
    
    # Add a simple root route for testing
    @app.route('/')
    def index():
        return '''
        <h1>University Resource App</h1>
        <p>Application is running!</p>
        <h3>Available Endpoints:</h3>
        <h4>Authentication API:</h4>
        <ul>
            <li>POST /api/auth/login - Login</li>
            <li>POST /api/auth/logout - Logout</li>
            <li>GET /api/auth/me - Get current user</li>
        </ul>
        <h4>Student API:</h4>
        <ul>
            <li>GET /api/student/dashboard - Student dashboard</li>
            <li>GET /api/student/browse - Browse resources</li>
            <li>GET /api/student/profile - Student profile</li>
        </ul>
        <h4>Lecturer API:</h4>
        <ul>
            <li>GET /api/lecturer/dashboard - Lecturer dashboard</li>
            <li>GET /api/lecturer/review/&lt;id&gt; - Get resource for review</li>
            <li>POST /api/lecturer/review/&lt;id&gt; - Review resource</li>
            <li>GET /api/lecturer/profile - Lecturer profile</li>
        </ul>
        <h4>Resources API:</h4>
        <ul>
            <li>POST /api/resources/upload - Upload resource</li>
            <li>GET /api/resources/download/&lt;id&gt; - Download resource</li>
            <li>GET /api/resources/categories - Get categories</li>
            <li>GET /api/resources/my-uploads - My uploads</li>
        </ul>
        <p><a href="/auth/login">Web Login</a></p>
        '''
    
    return app
