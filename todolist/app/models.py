from app.database import get_db

class Task:
    def __init__(self, id_task=None, nombre=None, descripcion=None, fecha_creacion=None, completada=None, activa=None):
        self.id_task = id_task
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.completada = completada
        self.activa = activa

    # utilizamos un método estático para realizar las consultas
    # de las tareas y el estado de las mismas
    @staticmethod
    def __get_tasks_by_query(query):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    
        tasks = []
        for row in rows:
            tasks.append(
                Task(
                    id_task=row[0],
                    nombre=row[1],
                    descripcion=row[2],
                    fecha_creacion=row[3],
                    completada=row[4],
                    activa=row[5]
                )
            )
        cursor.close()
        return tasks

    @staticmethod
    def get_all_pending():
        return Task.__get_tasks_by_query(
            """
            SELECT * FROM tareas
            WHERE activa = True AND completada = False
            ORDER BY fecha_creacion DESC
            """
        )
    
    @staticmethod
    def get_all_completed():
        return Task.__get_tasks_by_query(
            """
            SELECT * FROM tareas
            WHERE activa = False AND completada = True
            ORDER BY fecha_creacion DESC
            """
        )
    
    @staticmethod
    def get_all_archived():
        return Task.__get_tasks_by_query(
            """
            SELECT * FROM tareas
            WHERE activa = False
            ORDER BY fecha_creacion DESC
            """
        )
    
    @staticmethod
    def get_by_id(id_task):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id=%s",(id_task,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            return Task(
                id_task=row[0],
                nombre=row[1],
                descripcion=row[2],
                fecha_creacion=row[3],
                completada=row[4],
                activa=row[5]
            )
        return None
    
    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_task: #actualizar tarea
            cursor.execute(
                """
                UPDATE tareas
                SET nombre = %s, descripcion = %s, completada = %s, activa = %s
                WHERE id = %s
                """,
                (self.nombre, self.descripcion, self.completada,self.activa, self.id_task))
        else: # Crea una tarea nueva
            cursor.execute(
                """
                INSERT INTO tareas
                (nombre, descripcion, fecha_creacion, completada, activa)
                VALUES(%s,%s,%s,%s,%s)
                """,
                (self.nombre,self.descripcion,self.fecha_creacion,self.completada,self.activa)
            )
            self.id_task = cursor.lastrowid
        db.commit()
        cursor.close()
    
    def delete(self): # No la elimina, cambia si está activa o no
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE tareas SET activa = False
            WHERE id = %s
            """,
            (self.id_task,)
        )
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id': self.id_task,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d'),
            'completada': self.completada,
            'activa': self.activa
        }