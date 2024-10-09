from flask import jsonify, request
from app.models import Usuario, Post, Tag, Categoria, Comentario, Posts_Tags, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime


def index():
    return jsonify({
        'message':"Bienvenido a la API Blog con gestión de usuarios, publicaciones y comentarios!."
    })

'''
CRUD DE USUARIO
'''
def register():
    data = request.get_json()
    usuario = Usuario(
        nombre = data['nombre'],
        apellido = data['apellido'],
        email = data['email'],
        usuario = data['usuario'],
        password_hash = data['contraseña'],
        rol = data['rol'],
        status = 'activo',
        fecha_registro = ['fecha de registro']
    )
    usuario.set_password_hash(data['contraseña'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'message':f'El/la usuario/a {data['usuario']} fue creado exitosamente.'}), 200

def login():
    data = request.get_json()
    usuario_login = Usuario.query.filter_by(usuario=data['usuario']).first()
    if usuario_login and usuario_login.check_password(data['contraseña']):
        access_token = create_access_token(identity=usuario_login.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message':'Inicio de sesión inválido'}), 401

@jwt_required()
def profile(user_id):
    usuario = Usuario.query.filter_by(id=user_id)
    if not usuario:
        return jsonify({'message':'El usuario no encontrado'}), 404
    return jsonify(usuario.serialize()), 200

#*******************Editar usuario PENDIENTE*******************


'''
CRUD DE POSTEOS
'''

# Buscar todos los posts
@jwt_required()
def get_all_post():
    autor_ident = get_jwt_identity()
    posts = Post.query.filter_by(autor_id=autor_ident).all()
    posts_json  = [{
        'id':post.id,'titulo':post.titulo,'contendio':post.contenido,
        'fecha de creacion':post.fecha_creacion,'categoria':post.categoria,
        'status':post.status_post,'autor':post.autor_id,'Ultima actualizacion':post.fecha_actualizacion
    } for post in posts]

    return jsonify(posts_json), 200

# Buscar un post
@jwt_required()
def get_post(post_id):
    #autor_ident = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    if not post:
        return jsonify({'message':'Posteo no encontrado.'}), 404
    return jsonify(post.serialize_post()), 200
    

# Creación de un post
@jwt_required()
def create_post():
    data = request.get_json()
    autor_id = get_jwt_identity()
    post = Post(
        titulo = data['titulo'],
        contenido = data.get('contenido'),
        autor_ident = autor_id,
        categoria_id = data['categoria'],
        status_post = data.get('status'),
        )
    db.session.add(post)
    db.session.commit()
    return jsonify({'message':'Post creado con éxito.'}), 200
    

# Edición de un post
@jwt_required()
def edit_post(post_id):
    user_ident = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(id=user_ident).first()
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return jsonify({'error':'Posteo inexistent.'}), 404
    
    if post.autor_id == usuario_logueado.id or usuario_logueado.rol == 'admin':
        data = request.get_json()
        post.titulo = data.get('titulo',post.titulo)
        post.contendio = data.get('contenido',post.contendio)
        post.status_post = data.get('status_post',post.status_post)
        post.categoria_id = data.get('categoria',post.categoria_id)
        post.fecha_actualizacion = data.get('Ultima actualizacion',post.fecha_actualizacion)
        db.session.commit()
        return jsonify({'message':'Usuario editado correctamente.'}), 200
    return jsonify({'error':'No autorizado.'}), 403