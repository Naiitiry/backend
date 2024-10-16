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
        rol = 'usuario',
        status = 'activo',
        fecha_registro = data.get('fecha_registro')
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
    usuario = Usuario.query.get_or_404(user_id)
    if not usuario:
        return jsonify({'message':'Usuario no encontrado'}), 404
    return jsonify(usuario.serialize()), 200

#******************* Editar usuario *******************
@jwt_required()
def edit_profile(user_id):
    user_id_jwt = get_jwt_identity()
    usuario = Usuario.query.get_or_404(user_id)
    usuario_logueado = Usuario.query.filter_by(id=user_id_jwt).first()
    if usuario:
        if usuario.id == usuario_logueado.id or usuario_logueado.rol == 'admin':
            data = request.get_json()
            usuario.nombre = data.get('nombre',usuario.nombre)
            usuario.apellido = data.get('apellido',usuario.apellido)
            usuario.usuario = data.get('usuario',usuario.usuario)
            usuario.email = data.get('email',usuario.email)
            db.session.commit()
            return jsonify({'message':f"Usuario {usuario.usuario} actualizaco con éxito"}), 200
        return jsonify({'error':'No autorizado'}), 403
    return jsonify({'error':'Usuario inexistente'}), 404

'''
CRUD DE POSTEOS
'''

# Buscar todos los posts
@jwt_required()
def get_all_post():
    posts = Post.query.all()
    posts_listados = [post.serialize_post() for post in posts]
    return jsonify({'Todos los posts':posts_listados}), 200

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
        autor_id = autor_id,
        # La categoria_id va con el ID, si ponemos con 
        # nombre arroja el error.
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
    post = Post.query.get_or_404(post_id)

    if not post:
        return jsonify({'error':'Posteo inexistente.'}), 404
    
    if post.autor_id == usuario_logueado.id or usuario_logueado.rol == 'admin':
        data = request.get_json()
        post.titulo = data.get('titulo',post.titulo)
        post.contenido = data.get('contenido',post.contenido)
        post.status_post = data.get('status_post',post.status_post)
        post.categoria_id = data.get('categoria',post.categoria_id)
        post.fecha_actualizacion = data.get('Ultima actualizacion',post.fecha_actualizacion)
        db.session.commit()
        return jsonify({'message':'Posteo editado correctamente.'}), 200
    return jsonify({'error':'No autorizado.'}), 403

# Eliminar Post
@jwt_required()
def delete_post(post_id):
    user_ident = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(id=user_ident).first()
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({'error':'El post solicitado no existe.'}),404
    if usuario_logueado.id == post.autor_id or usuario_logueado.rol == 'admin':
        post.delete()
        return jsonify({'message':'Posteo eliminado correctamente.'}), 200
    return jsonify({'error':'No posees los permisos para eliminar el post'}), 403

'''
CRUD DE CATEGORIAS
'''

@jwt_required()
def get_all_categories():
    categorias = Categoria.query.all()
    categorias_listada = [categoria.serialize_categorias() for categoria in categorias]
    return jsonify({'categorias':categorias_listada}), 200

@jwt_required()
def create_categories():
    user_ident = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(id=user_ident).first()
    
    if usuario_logueado.rol != 'admin':
        return jsonify({'error':'No tienes los permisos para ejecutar la tarea.'}), 403
    
    data = request.get_json()
    nombre_categoria = data.get('nombre')

    categoria_existente = Categoria.query.filter_by(nombre=nombre_categoria).first()
    if categoria_existente:
        return jsonify({'error':'Categoría ya existente.'}), 400
    
    nueva_categoria = Categoria(nombre_categoria)
    db.session.add(nueva_categoria)
    db.session.commit()
    return jsonify({'message':f'Categoría {nombre_categoria} creada exitosamente.'}), 201

@jwt_required()
def edit_categorie(cate_id):
    user_ident = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(id=user_ident).first()
    categoria = Categoria.query.get_or_404(cate_id)

    if usuario_logueado.rol != 'admin':
        return jsonify({'error':'No tienes los permisos para ejecutar la tarea.'}), 403
    
    data = request.get_json()
    categoria.nombre = data.get('nombre',Categoria.nombre)
    db.session.commit()
    return jsonify({'message':'Categoría editada exitosamente.'}), 200

"""
CRUD DE COMENTARIOS
"""

@jwt_required()
def get_all_comments():
    comentarios = Comentario.query.all()
    comentarios_listado = [comentario.serialize() for comentario in comentarios]
    return jsonify({'Todos los comentarios':comentarios_listado}), 200

@jwt_required()
def create_comments():
    data = request.get_json()
    autor_id = get_jwt_identity()
    post_id = data.get('post_id')
    post = Post.query.get_or_404(post_id)
    comment = Comentario(
        contenido = data.get('contenido'),
        post_id = post.id,
        autor_id = autor_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message':'Comentario creado con éxito.'}), 201

@jwt_required()
def edit_comments(comment_id):
    user_ident = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(id=user_ident).first()
    comentario = Comentario.query.filter_by(id=comment_id).first()

    if not comentario:
        return jsonify({'error':'Comentario inexistente.'}), 404
    
    if comentario.autor_id == usuario_logueado.id or usuario_logueado.rol == 'admin':
        data = request.get_json()
        comentario.contenido = data.get('contenido',comentario.contenido)
        db.session.commit()
        return jsonify({'message':'Comentario editado correctamente.'}), 200
    return jsonify({'error':'No autorizado.'}), 403

@jwt_required()
def delete_comments(comment_id):
    user_ident = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(id=user_ident).first()
    comentario = Comentario.query.filter_by(id=comment_id).first()

    if not comentario:
        return jsonify({'error':'Comentario inexistente.'}), 404
    
    if comentario.autor_id == usuario_logueado.id or usuario_logueado.rol == 'admin':
        comentario.delete()
        return jsonify({'message':'Comentario eliminado exitosamente.'}), 200
    return jsonify({'error':'No tienes para eliminar el comentario.'}), 404