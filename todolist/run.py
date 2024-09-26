from flask import Flask
from app.database import *
from app.views import *
from flask_cors import CORS

app = Flask(__name__)

# CRUD

app.route('/', methods=['GET']) (index)
app.route('/api/tasks/pending',methods=['GET']) (get_pending_tasks)
app.route('/api/tasks/completed',methods=['GET']) (get_completed_tasks)
app.route('/api/tasks/archived',methods=['GET']) (get_archived_tasks)

app.route('/api/tasks/fetch/<int:task_id>',methods=['GET']) (get_task)

app.route('/api/tasks/create',methods=['POST']) (create_task)
app.route('/api/tasks/update/<int:task_id>',methods=['PUT']) (update_task)

app.route('/api/tasks/archive/<int:task_id>',methods=['DELETE'])(archive_task)
app.route('/api/tasks/complete/set/<int:task_id>',methods=['PUT'])(set_complete_task)
app.route('/api/tasks/complete/reset/<int:task_id>',methods=['PUT'])(reset_complete_task)

# I - Primero va la creación de las tablas
create_table_tareas()

# II - conexión a la BBDD
init_app(app)

# III - CORS
CORS(app)

# Test conexión a BBDD
# test_connection()
# conecta sin problemas!

if __name__ == "__main__":
    app.run(debug=True)