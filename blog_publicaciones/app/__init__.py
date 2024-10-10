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

    from app.models import Usuario, Tag, Post, Posts_Tags, Comentario, Categoria
    from app.views import index, register, login, profile, get_all_post, get_post, create_post, edit_post

    # Gestión de usuario
    app.route('/',methods=['GET'])(index)
    app.route('/api/register',methods=['POST'])(register)
    app.route('/api/login',methods=['POST'])(login)
    app.route('/api/fetch/<int:user_id>',methods=['GET'])(profile)

    # Gestión de publicaciones
    app.route('/api/publicaciones',methods=['GET'])(get_all_post)
    app.route('/api/publicacion/<int:post_id>',methods=['GET'])(get_post)
    app.route('/api/crear_publicacion',methods=['POST'])(create_post)
    app.route('/api/editar_publicacion/<int:post_id>',methods=['PUT'])(edit_post)

    # Creación de categorías, unicamente ADMINS
    
    return app

# para correr correctamente la migración de SQLAlchemy
# flask --app run.py db init

# cuando pide completar 'alembic.ini', se debe poner lo siguiente (cambiandolo por los datos propios)
# sqlalchemy.url = postgresql://tu_usuario:tu_contraseña@localhost/tu_base_de_datos

# los cuales, si se configuró previamente, están en el .env