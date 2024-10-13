from sqlalchemy import Enum, func
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    apellido = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(150),nullable=False,unique=True)
    usuario = db.Column(db.String(150),nullable=False,unique=True)
    password_hash = db.Column(db.String(350),nullable=False)
    rol = db.Column(Enum('admin','usuario',name='rol'),default='usuario',nullable=True)
    status = db.Column(Enum('activo','inactivo','bloqueado',name='status'),default='activo',nullable=True)
    fecha_registro = db.Column(db.DateTime,default=func.now(),nullable=True)

    # Relación usuario - posts
    posts = db.relationship('Post',backref='autor',lazy=True)

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
        post_totales = Post.query.filter_by(autor_id=self.id).count()
        return{
            'id':self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'usuario':self.usuario,
            'email': self.email,
            'rol': self.rol,
            'status': self.status,
            'fecha_registro':self.fecha_registro.strftime('%d/%m/%Y') if self.fecha_registro else None,
            'post_totales': post_totales
        }

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String(150),nullable=False)
    contenido = db.Column(db.Text,nullable=False)
    fecha_creacion = db.Column(db.DateTime,default=func.now())
    fecha_actualizacion = db.Column(db.DateTime,default=func.now(),onupdate=func.now())
    autor_id = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)
    categoria_id = db.Column(db.Integer,db.ForeignKey('categoria.id'),nullable=False)
    status_post = db.Column(Enum('borrador','publicado',name='status_post'),default='borrador',nullable=True)

    def serialize_post(self):
        return{
            'id':self.id, 'titulo':self.titulo, 'contenido':self.contenido,
            'fecha de creacion':self.fecha_creacion.strftime('%d/%m/%Y'),
            'Ultima actualización':self.fecha_actualizacion.strftime('%d/%m/%Y'),
            'id del creador':self.autor_id,'id de categoría':self.categoria_id,
            'Estado post':self.status_post
        }

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer,primary_key=True)
    contenido = db.Column(db.Text,nullable=False)
    fecha_creacion = db.Column(db.DateTime,default=func.now())
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    autor_id = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)

    def serialize(self):
        return{
            'contenido':self.contenido,
            'fecha de creación':self.fecha_creacion,
            
        }

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(150),unique=True,nullable=False)

    def __init__(self,nombre):
        self.nombre = nombre

    def serialize_categorias(self):
        return{
            'id':self.id,
            'nombre':self.nombre
        }

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(150),unique=True,nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

class Posts_Tags(db.Model):
    __tablename__ = 'posts_tags'
    post_id = db.Column(db.Integer,db.ForeignKey('post.id', ondelete='CASCADE'),primary_key=True,nullable=False)
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id', ondelete='CASCADE'),primary_key=True,nullable=False)