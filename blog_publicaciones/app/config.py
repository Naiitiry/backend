import os
from flask import g
from dotenv import load_dotenv


class Config():
    # Leemos el archivo .env
    load_dotenv()
    # Configuración de DDBB con variables de entorno
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv('FULL_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'myjwtsecretkey')
