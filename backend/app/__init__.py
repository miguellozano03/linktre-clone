from flask import Flask 
from flask_migrate import Migrate
from .config.config import Config
from .config.database import db
from .routes.users import users_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)

    @app.route("/testing")
    def test():
        return {"message": "It' works"}
    
    return app