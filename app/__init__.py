from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.controllers.session_controller import session_bp
    app.register_blueprint(session_bp, url_prefix='/api')
    
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.controllers.web_session_controller import web_session_bp
    app.register_blueprint(web_session_bp)

    return app
