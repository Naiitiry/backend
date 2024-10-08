from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from . import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db.Model):
    uid = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    apellido = db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(150),nullable=False,unique=True)
    password_hash = db.Column(db.String(350),nullable=False)
    edad = db.Column(db.Integer,nullable=False)
    telefono = db.Column(db.String(100),nullable=False)
    usuario = db.Column(db.String(150),nullable=False,unique=True)
    fecha_nacimiento = db.Column(db.Date,nullable=True)

    usuario_rol = db.Column(Enum('admin','usuario', name='usuario_rol'), default='usuario',nullable=False)
    status = db.Column(Enum('activo','inactivo','bloqueado',name='status'), default='activo',nullable=False)


    def set_password_hash(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def delete(self):
        self.status = 'inactivo'

    def activate(self):
        self.status = 'activo'

    def block(self):
        self.status = 'bloqueado'

    def serialize(self):
        return {
            'id': self.uid,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%d/%m/%Y') if self.fecha_nacimiento else None,
            'usuario_rol': self.usuario_rol,
            'status': self.status
        }