from flask import Flask
from app.database import *
from app.views import *

app = Flask(__name__)



if __name__ == "__main__":
    app.run(debug=True)