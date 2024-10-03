from flask import jsonify, request
#from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Usuario
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
        contraseña_hash=data['contraseña'],
        fecha_nacimiento=data['fecha_nacimiento'],
        domicilio=data['domicilio'],
        usuario_role='usuario',
        status='activo'
        )
    usuario.set_password_hash(data['contraseña'])
    usuario.save()
    return jsonify({'message': f'Usuario {data['usuario']}, creado correctamente.'}), 200

# Logear a traves del Email,
# Tambien, en un futuro, modificar para que el username
# sea otra alternativa
def login():
    data = request.get_json()
    usuario = Usuario.get_by_email(data['email'])
    if usuario and usuario.check_password(data['contraseña']):
        access_token = create_access_token(identity={'username':usuario.usuario,'role':usuario.usuario_role,'id':usuario.id_user})
        return jsonify(access_token=access_token), 200
    return jsonify({'error':'Inicio de sesión inválido'}), 401

@jwt_required()
def profile(id_user):
    current_user= get_jwt_identity()
    current_user_id = current_user['id']
    usuario = Usuario.get_by_id(id_user)
    if not usuario:
        return jsonify({'message':'Usuario no encontrado'})
    return jsonify(usuario.serialize()), 200

def ayuda():
    if request.method == 'PUT':
        pass
        # if current_user_id == usuario.id_user:
        #     data = request.get_json()
        #     usuario.nombre = data.get('nombre',usuario.nombre)
        #     usuario.apellido = data.get('apellido',usuario.apellido)
        #     usuario.edad = data.get('edad',usuario.edad)
        #     usuario.email = data.get('email',usuario.email)
        #     usuario.telefono = data.get('telefono',usuario.telefono)
        #     usuario.fecha_nacimiento = data.get('fecha_nacimiento',usuario.fecha_nacimiento)
        #     usuario.domicilio = data.get('domicilio',usuario.domicilio)
        #     usuario.usuario_role = data.get('usuario_role',usuario.usuario_role)
        #     usuario.status = data.get('status',usuario.status)
        #     usuario.save()
        #     return jsonify({'message':'Usuario actualizado!.'}), 200
        # return jsonify({'error':'No autorizado'}),403
    
    # elif request.method == 'DELETE':
    #     if current_user['usuario_role'] == 'admin':
    #         usuario.delete()
    #         return jsonify({'message':'El usuario ha sido inhabilitado.'}), 200
    #     return jsonify({'error':'No autorizado'}),403