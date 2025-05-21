import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_change_me') #Pour session
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/projetweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
