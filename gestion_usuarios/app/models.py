from app.database import get_db
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario:
    def __init__(self, id_user=None, nombre=None, apellido=None,
                edad=None, email=None, telefono=None, usuario=None,
                contraseña_hash=None, fecha_nacimiento=None, domicilio=None,
                usuario_role=None, status=None):
        self.id_user = id_user
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.email = email
        self.telefono = telefono
        self.usuario = usuario
        self.contraseña_hash = contraseña_hash
        self.fecha_nacimiento = fecha_nacimiento
        self.domicilio = domicilio
        self.usuario_role = usuario_role
        self.status = status

    def set_password_hash(self, contraseña_hash):
        self.contraseña_hash=generate_password_hash(contraseña_hash)

    def check_password(self, contraseña_hash):
        return check_password_hash(self.contraseña_hash,contraseña_hash)

    @staticmethod
    def __get_users_by_query(query):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        users = []
        for row in rows:
            users.append(
                Usuario(
                    id_user=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    edad=row[3],
                    email=row[4],
                    telefono=row[5],
                    usuario=row[6],
                    contraseña_hash=row[7],
                    fecha_nacimiento=row[8],
                    domicilio=row[9],
                    usuario_role=row[10],
                    status=row[11],
                )
            )
        cursor.close()
        return users
    
    @staticmethod
    def get_by_id(id_user):
        db = get_db()
        cursor = db.cursor
        cursor.execute(
            "SELECT * FROM usuarios WHERE id=%s",(id_user,)
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Usuario(
                id_user=row[0],
                nombre=row[1],
                apellido=row[2],
                edad=row[3],
                email=row[4],
                telefono=row[5],
                usuario=row[6],
                contraseña_hash=row[7],
                fecha_nacimiento=row[8],
                domicilio=row[9],
                usuario_role=row[10],
                status=row[11],
            )
        return None
    
    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_user: #actualizar usuario
            cursor.execute(
                """
                UPDATE usuarios
                SET nombre = %s, apellido = %s, edad = %s, 
                email = %s, telefono = %s, fecha_nacimiento = %s,
                domicilio = %s, usuario_role = %s, status = %s
                WHERE id = %s
                """,
                (self.nombre, self.apellido, self.edad, self.email, self.telefono,
                self.fecha_nacimiento, self.domicilio, self.usuario_role, self.status)
            )
        else: # En caso de que no exista el usuario id (id_user) crea uno nuevo
            cursor.execute(
                """
                INSERT INTO usuarios
                (nombre, apellido, edad, email, telefono, usuario, contraseña_hash, fecha_nacimiento, domicilio, usuario_role, status)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (self.nombre, self.apellido, self.edad, self.email, self.telefono, self.usuario, self.contraseña_hash, self.fecha_nacimiento, self.domicilio, self.usuario_role, self.status)
            )
            self.id_user = cursor.lastrowid
        db.commit()
        cursor.close()

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE usuarios SET status = inactivo
            WHERE id = %s
            """,
            (self.id_user,)
        )
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id': self.id_user,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_nacimiento': self.fecha_nacimiento,
            'domicilio': self.domicilio,
            'usuario_role': self.usuario_role,
            'status': self.status
        }