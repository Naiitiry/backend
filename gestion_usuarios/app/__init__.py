import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    from app.models import Usuario
    from app.views import register,login,logout,index,profile,edit_profile
    # Rutas de login, register y profile
    app.route('/', methods=['GET'])(index)

    app.route('/session/register', methods=['POST']) (register)
    app.route('/session/login', methods=['POST']) (login)
    app.route('/session/profile/<int:id_user>', methods=['GET']) (profile)
    app.route('/session/profile/edit/<int:id_user>', methods=['PUT']) (edit_profile)
    

    return app