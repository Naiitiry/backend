import os
from flask import Flask
from app.database import *
from app.views import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Rutas de login, register y profile
app.route('/', methods=['GET'])(index)

app.route('/api/users/register', methods=['POST']) (register)
app.route('/api/users/login', methods=['POST']) (login)
app.route('/api/users/profile/<int:id_user>', methods=['GET','PUT','DELETE']) (profile)





# Inicio de la app
init_app(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)