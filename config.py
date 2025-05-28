import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_change_me') #Pour session
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/projetweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Configuration Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ton.email@gmail.com'
    MAIL_PASSWORD = 'ton_mot_de_passe' 