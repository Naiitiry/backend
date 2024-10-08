from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app,db)
jwt.init_app(app)

@app.route('/',methods=['GET'])
def index():
    return 'Hola mundo!'

if __name__=="__main__":
    app.run(debug=True)