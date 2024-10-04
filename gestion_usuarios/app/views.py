from flask import jsonify, request
#from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Usuario, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def index():
    return jsonify({
        'mensage':'Bienvenido a la API de Gestión de Usuarios.'
    })

def register():
    data = request.get_json()
    usuario = Usuario(
        nombre=data['nombre'],
        apellido=data['apellido'],
        edad=data['edad'],
        email=data['email'],
        telefono=data['telefono'],
        usuario=data['usuario'],
        password_hash=data['contraseña'],
        fecha_nacimiento=data['fecha_nacimiento'],
        usuario_rol='usuario',
        status='activo'
        )
    usuario.set_password_hash(data['contraseña'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'message': f'Usuario {data['usuario']}, creado correctamente.'}), 200

# Logear a traves del nombre de usuario
def login():
    data = request.get_json()
    usuario_login = Usuario.query.filter_by(usuario=data['usuario']).first()
    if usuario_login and usuario_login.check_password(data['contraseña']):
        access_token = create_access_token(identity=usuario_login.uid)
        return jsonify(access_token=access_token), 200
    return jsonify({'error':'Inicio de sesión inválido'}), 401

@jwt_required()
def logout():
    db.session.close()
    return jsonify({'message':'Cierre de sesión exitoso.'})

@jwt_required()
def profile(id_user):
    id_user = get_jwt_identity()
    usuario = Usuario.query.filter_by(uid=id_user).first()
    if not usuario:
        return jsonify({'message':'Usuario no encontrado'})
    return jsonify(usuario.serialize()), 200

@jwt_required()
def edit_profile(id_user):
    id_user = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(uid=id_user).first()
    usuario = Usuario.query.filter_by(uid=id_user).first()
    if usuario:
        if usuario.uid != usuario_logueado.uid and usuario_logueado.usuario_rol != 'admin':
            data = request.get_json()
            usuario.nombre = data.get('nombre',usuario.nombre)
            usuario.apellido = data.get('apellido',usuario.apellido)
            usuario.edad = data.get('edad',usuario.edad)
            usuario.email = data.get('email',usuario.email)
            usuario.telefono = data.get('telefono',usuario.telefono)
            usuario.fecha_nacimiento = data.get('fecha_nacimiento',usuario.fecha_nacimiento)
            usuario.usuario_rol = data.get('usuario_rol',usuario.usuario_rol)
            usuario.status = data.get('status',usuario.status)
            db.session.commit()
            return jsonify({'message':'Usuario actualizado!.'}), 200
        return jsonify({'error':'No autorizado'}),403
    return jsonify({'error':'Usuario inexistente'}), 404

@jwt_required()
def archive_profile(id_user):
    id_user = get_jwt_identity()
    usuario_logueado = Usuario.query.filter_by(uid=id_user).first()
    usuario = Usuario.query.filter_by(uid=id_user).first()
    if usuario:
        if usuario.uid != usuario_logueado.uid and usuario_logueado.usuario_rol != 'admin':
            usuario.delete()
            return jsonify({'message':'Usuario deshabilitado.'}), 200
        return jsonify({'error':'No autorizado'}),403
    return jsonify({'error':'Usuario inexistente'}), 404
    # elif request.method == 'DELETE':
    #     if current_user['usuario_role'] == 'admin':
    #         usuario.delete()
    #         return jsonify({'message':'El usuario ha sido inhabilitado.'}), 200
    #     return jsonify({'error':'No autorizado'}),403