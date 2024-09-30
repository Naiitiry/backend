import os
import psycopg2
from flask import g
from dotenv import load_dotenv

# Leemos el archivo .env
load_dotenv()

# Configuración de DDBB con variables de entorno
DATABASE_CONFIG = {
    'user': os.getenv('DB_USERNAME'),        
    'password': os.getenv('DB_PASSWORD'),     
    'host': os.getenv('DB_HOST'),            
    'database': os.getenv('DB_NAME'),        
    'port': os.getenv('DB_PORT', 5432)   
}

# Test de la BBDD
def test_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    conn.commit()
    cur.close()
    conn.close()

# Función para obtener la BBDD
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(**DATABASE_CONFIG)
    return g.db

def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

# Creación de BBDD
"""
Ya que Postgresql no posee ENUM, se genera con TYPE
los 3 STATUS y los 3 ROLES de un usuario.
"""
def create_table_usuarios():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TYPE usuario_role AS ENUM('admin','usuario','anonimo');
        CREATE TYPE status AS ENUM('activo','inactivo','bloqueado');

        CREATE TABLE IF NOT EXISTS Usuarios(
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            apellido VARCHAR(150) NOT NULL,
            edad INT CHECK (edad>10),
            email VARCHAR(255) NOT NULL,
            telefono VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) NOT NULL,
            contraseña_hash VARCHAR(300) NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            domicilio TEXT NOT NULL,
            usuario_role usuario_role DEFAULT 'usuario',
            status status DEFAULT 'activo'
        );
        """
    )
    conn.commit()
    cur.close()