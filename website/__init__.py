from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'obfdbgbkpwfduvbfd'  # Secret key for session encryption
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Path to SQLite DB

    db.init_app(app)  # Initialize the database with the app

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import Doctor, Patient
    
    # Create the database
    create_db(app)

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Where to redirect if the user is not logged in
    login_manager.init_app(app)

    # Define user loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return Doctor.query.get(int(id))  # Load user by ID (doctor ID here)
    
    @app.context_processor
    def inject_user():
        return dict(user=current_user)  # Fix: Correct indentation

    return app

# Function to create the database if it doesn't exist
def create_db(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():  # Ensure app context for db.create_all
            db.create_all()  # Create database tables
        print('Created Database!')
