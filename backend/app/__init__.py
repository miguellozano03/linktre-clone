from flask import Flask 
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .config import Config, db
from .users.routes import users_bp
from .links.routes import links_bp
from .auth import auth_bp

migrate = Migrate()
jwt = JWTManager()

def create_app(config_object = Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)
    app.register_blueprint(links_bp)
    app.register_blueprint(auth_bp)
    
    return app