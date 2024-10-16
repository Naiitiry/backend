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
    from app.views import (index,register, login, profile, 
        get_all_post, get_post, create_post, edit_post, 
        edit_profile, create_categories,get_all_categories,
        edit_categorie,delete_post, create_comments, edit_comments, 
        delete_comments,get_all_comments
        )

    # Gestión de usuario
    app.route('/',methods=['GET'])(index)
    app.route('/api/register',methods=['POST'])(register)
    app.route('/api/login',methods=['POST'])(login)
    app.route('/api/fetch/<int:user_id>',methods=['GET'])(profile)
    app.route('/api/edit/<int:user_id>',methods=['PUT'])(edit_profile)

    # Gestión de publicaciones
    app.route('/api/publicaciones',methods=['GET'])(get_all_post)
    app.route('/api/publicacion/<int:post_id>',methods=['GET'])(get_post)
    app.route('/api/crear_publicacion',methods=['POST'])(create_post)
    app.route('/api/editar_publicacion/<int:post_id>',methods=['PUT'])(edit_post)
    app.route('/api/publicacion/eliminar_post/<int:post_id>',methods=['DELETE'])(delete_post)

    # Creación de categorías, unicamente ADMINS
    app.route('/api/categorias',methods=['GET'])(get_all_categories)
    app.route('/api/crear_categoria',methods=['POST'])(create_categories)
    app.route('/api/editar_categoria/<int:cate_id>',methods=['PUT'])(edit_categorie)


    # Gestión de comentarios
    app.route('/api/comentarios',methods=['GET'])(get_all_comments)
    app.route('/api/crear_comentario',methods=['POST'])(create_comments)
    app.route('/api/editar_comentario/<int:comment_id>',methods=['PUT'])(edit_comments)
    app.route('/api/eliminar_comentario/<int:comment_id>',methods=['DELETE'])(delete_comments)


    return app

# para correr correctamente la migración de SQLAlchemy
# flask --app run.py db init
# flask --app run.py db migrate
# flask --app run.py db upgrade

# cuando pide completar 'alembic.ini', se debe poner lo siguiente (cambiandolo por los datos propios)
# sqlalchemy.url = postgresql://tu_usuario:tu_contraseña@localhost/tu_base_de_datos

# los cuales, si se configuró previamente, están en el .env