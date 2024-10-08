from sqlalchemy import Enum, func
from run import db
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.Sting(100),nullable=False)
    apellido = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(150),nullable=False)
    usuario = db.Column(db.String(150),nullable=False)
    password_hash = db.Column(db.String(350),nullable=False)
    rol = db.Column(Enum('admin','usuario',name='rol'),default='usuario',nullable=True)
    status = db.Column(Enum('activo','inactivo','bloqueado',name=status),default='activo',nullable=True)
    fecha_registro = db.Column(db.Datetime,default=func.now(),nullable=True)

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
        return{
            'id':self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'usuario':self.usuario,
            'email': self.email,
            'rol': self.rol,
            'status': self.status,
            'fecha_registro':self.fecha_registro
        }

class Posts(db.Model):
    pass

class Comentarios(db.Model):
    pass

class Categorias(db.Model):
    pass

class Tags(db.Model):
    pass

class Posts_Tags(db.Model):
    pass