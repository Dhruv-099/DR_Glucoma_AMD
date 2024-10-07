from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
import logging

# Initialize extensions
db = SQLAlchemy()
DB_NAME = 'database.db'
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    from .models import Doctor, Patient
    doctor = Doctor.query.get(int(id))
    if doctor:
        return doctor
    return Patient.query.get(int(id))

# Function to create the database if it doesn't exist
def create_db(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():  # Ensure app context for db.create_all
            db.create_all()  
        app.logger.info('Created Database!')
    else:
        app.logger.info('Database already exists.')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'obfdbgbkpwfduvbfd'  # Secret key for session encryption
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Path to SQLite DB

    db.init_app(app)  # Initialize the database with the app
    
    # Setup logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)

    app.logger.debug("App created")

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
    login_manager.login_view = 'auth.login'  # Where to redirect if the user is not logged in
    login_manager.init_app(app)

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)  # Inject current_user into all templates

    return app