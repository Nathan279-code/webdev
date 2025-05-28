from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail() 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "oau4i]V4;v9D~w.u75Mr=<=2v=e/h(>.5s'ak@zCmWx3f~,oOuJt:#!#lwk*?x&"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
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