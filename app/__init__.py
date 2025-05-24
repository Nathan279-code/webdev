from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  

    from app.models import models
    from app.models.models import Utilisateur
    from app import routes  #Importation route

    @login_manager.user_loader
    def load_user(user_id):
        return Utilisateur.query.get(user_id)

    app.register_blueprint(routes.main)
    app.register_blueprint(routes.auth)

    with app.app_context():
        db.create_all()

    return app
