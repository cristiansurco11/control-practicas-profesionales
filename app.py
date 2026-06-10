from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "una_clave_secreta_mucho_mas_larga_y_segura_para_el_proyecto_2026"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "practicas_db"
#app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
jwt = JWTManager(app) 

@app.route('/')
def inicio():
    return f"<h2>Servidor Flask en ejecucion :)</h2>"
    #return render_template('index.html')
    #return render_template('login.html')

@app.route('/testdb')
def test():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1")
    return "¡Conexión a la Base de Datos exitosa!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == '12345':
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
        
    return jsonify({"error": "Credenciales incorrectas"}), 401


@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_estudiante, nombre, apellido, carrera, correo, telefono FROM estudiantes")
    datos = cursor.fetchall()
    cursor.close()

    if not datos:
        return jsonify({"mensaje": "No existen estudiantes registrados"}), 404
   
    estudiantes = [{"id_estudiante": f[0], "nombre": f[1], "apellido": f[2], "carrera": f[3], "correo": f[4], "telefono": f[5]} for f in datos]
    return jsonify(estudiantes), 200

@app.route('/estudiantes/<int:id>', methods=['GET'])
def estudiante_id(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_estudiante, nombre, apellido, carrera, correo, telefono FROM estudiantes WHERE id_estudiante = %s", (id,))
    f = cursor.fetchone()
    cursor.close()

    if f is None:
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404
   
    estudiante = {"id_estudiante": f[0], "nombre": f[1], "apellido": f[2], "carrera": f[3], "correo": f[4], "telefono": f[5]}
    return jsonify(estudiante), 200

@app.route('/estudiantes', methods=['POST'])
@jwt_required()
def crear_estudiante():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    carrera = data.get('carrera')
    correo = data.get('correo')
    telefono = data.get('telefono')
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO estudiantes (nombre, apellido, carrera, correo, telefono) VALUES (%s, %s, %s, %s, %s)", 
                   (nombre, apellido, carrera, correo, telefono))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": "Estudiante insertado con éxito"}), 201

@app.route('/estudiantes/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_estudiante(id):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    carrera = data.get('carrera')
    correo = data.get('correo')
    telefono = data.get('telefono')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_estudiante FROM estudiantes WHERE id_estudiante = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404

    sql = "UPDATE estudiantes SET nombre = %s, apellido = %s, carrera = %s, correo = %s, telefono = %s WHERE id_estudiante = %s"
    cursor.execute(sql, (nombre, apellido, carrera, correo, telefono, id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": f"Estudiante con ID {id} modificado con éxito"}), 200

@app.route('/estudiantes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_estudiante(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_estudiante FROM estudiantes WHERE id_estudiante = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404

    try:
        cursor.execute("DELETE FROM estudiantes WHERE id_estudiante = %s", (id,))
        mysql.connection.commit()
    except Exception:
        cursor.close()
        return jsonify({"mensaje": "No se puede eliminar el estudiante porque tiene prácticas asignadas"}), 400

    cursor.close()
    return jsonify({"mensaje": f"Estudiante con ID {id} eliminado con éxito"}), 200

@app.route('/instituciones', methods=['GET'])
def listar_instituciones():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_institucion, nombre, direccion, telefono, responsable FROM instituciones")
    datos = cursor.fetchall()
    cursor.close()

    if not datos:
        return jsonify({"mensaje": "No existen instituciones registradas"}), 404
   
    instituciones = [{"id_institucion": f[0], "nombre": f[1], "direccion": f[2], "telefono": f[3], "responsable": f[4]} for f in datos]
    return jsonify(instituciones), 200

@app.route('/instituciones', methods=['POST'])
@jwt_required()
def crear_institucion():
    data = request.get_json()
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    telefono = data.get('telefono')
    responsable = data.get('responsable')
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO instituciones (nombre, direccion, telefono, responsable) VALUES (%s, %s, %s, %s)", 
                   (nombre, direccion, telefono, responsable))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": "Institución insertada con éxito"}), 201

@app.route('/instituciones/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_institucion(id):
    data = request.get_json()
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    telefono = data.get('telefono')
    responsable = data.get('responsable')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_institucion FROM instituciones WHERE id_institucion = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"mensaje": "Institución no encontrada"}), 404

    sql = "UPDATE instituciones SET nombre = %s, direccion = %s, telefono = %s, responsable = %s WHERE id_institucion = %s"
    cursor.execute(sql, (nombre, direccion, telefono, responsable, id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": f"Institución con ID {id} modificada con éxito"}), 200

@app.route('/instituciones/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_institucion(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_institucion FROM instituciones WHERE id_institucion = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"mensaje": "Institución no encontrada"}), 404

    try:
        cursor.execute("DELETE FROM instituciones WHERE id_institucion = %s", (id,))
        mysql.connection.commit()
    except Exception:
        cursor.close()
        return jsonify({"mensaje": "No se puede eliminar la institución porque tiene prácticas vinculadas"}), 400

    cursor.close()
    return jsonify({"mensaje": f"Institución con ID {id} eliminada con éxito"}), 200


@app.route('/practicas', methods=['GET'])
def listar_practicas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_practica, id_estudiante, id_institucion, fecha_inicio, fecha_fin, horas, estado FROM practicas")
    datos = cursor.fetchall()
    cursor.close()

    if not datos:
        return jsonify({"mensaje": "No existen prácticas registradas"}), 404
   
    practicas = [{
        "id_practica": f[0], "id_estudiante": f[1], "id_institucion": f[2],
        "fecha_inicio": str(f[3]), "fecha_fin": str(f[4]) if f[4] else None,
        "horas": f[5], "estado": f[6]
    } for f in datos]
    return jsonify(practicas), 200

@app.route('/practicas', methods=['POST'])
@jwt_required()
def registrar_practica():
    data = request.get_json()
    id_estudiante = data.get('id_estudiante')
    id_institucion = data.get('id_institucion')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    horas = data.get('horas')
    estado = data.get('estado')
    
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO practicas (id_estudiante, id_institucion, fecha_inicio, fecha_fin, horas, estado) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_estudiante, id_institucion, fecha_inicio, fecha_fin, horas, estado))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": "Práctica registrada con éxito"}), 201

@app.route('/practicas/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_practica(id):
    data = request.get_json()
    id_estudiante = data.get('id_estudiante')
    id_institucion = data.get('id_institucion')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    horas = data.get('horas')
    estado = data.get('estado')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_practica FROM practicas WHERE id_practica = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"mensaje": "Práctica no encontrada"}), 404

    sql = """UPDATE practicas SET id_estudiante = %s, id_institucion = %s, fecha_inicio = %s, 
             fecha_fin = %s, horas = %s, estado = %s WHERE id_practica = %s"""
    cursor.execute(sql, (id_estudiante, id_institucion, fecha_inicio, fecha_fin, horas, estado, id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": f"Práctica con ID {id} modificada con éxito"}), 200

@app.route('/practicas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_practica(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_practica FROM practicas WHERE id_practica = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"mensaje": "Práctica no encontrada"}), 404

    try:
        cursor.execute("DELETE FROM practicas WHERE id_practica = %s", (id,))
        mysql.connection.commit()
    except Exception:
        cursor.close()
        return jsonify({"mensaje": "No se puede eliminar la práctica porque posee observaciones registradas"}), 400
        
    cursor.close()
    return jsonify({"mensaje": f"Práctica con ID {id} eliminada con éxito"}), 200

@app.route('/observaciones', methods=['GET'])
def listar_observaciones():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_observacion, id_practica, descripcion, fecha FROM observaciones")
    datos = cursor.fetchall()
    cursor.close()

    if not datos:
        return jsonify({"mensaje": "No existen observaciones registradas"}), 404

    obs = [{"id_observacion": f[0], "id_practica": f[1], "descripcion": f[2], "fecha": str(f[3])} for f in datos]
    return jsonify(obs), 200

@app.route('/observaciones', methods=['POST'])
@jwt_required()
def crear_observacion():
    data = request.get_json()
    id_practica = data.get('id_practica')
    descripcion = data.get('descripcion')
    fecha = data.get('fecha')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO observaciones (id_practica, descripcion, fecha) VALUES (%s, %s, %s)", 
                   (id_practica, descripcion, fecha))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"mensaje": "Observación guardada con éxito"}), 201

@app.route('/estudiantes/<int:id_estudiante>/practicas', methods=['GET'])
def practicas_por_estudiante(id_estudiante):
    cursor = mysql.connection.cursor()
    sql = """
        SELECT p.id_practica, i.nombre AS institucion, p.fecha_inicio, p.estado 
        FROM practicas p
        JOIN instituciones i ON p.id_institucion = i.id_institucion
        WHERE p.id_estudiante = %s
    """
    cursor.execute(sql, (id_estudiante,))
    datos = cursor.fetchall()
    cursor.close()
    
    if not datos:
        return jsonify({"mensaje": "Este estudiante no cuenta con prácticas asignadas"}), 404
        
    historial = [{"id_practica": f[0], "institucion": f[1], "fecha_inicio": str(f[2]), "estado": f[3]} for f in datos]
    return jsonify(historial), 200

@app.route('/practicas/<int:id_practica>/observaciones', methods=['GET'])
def observaciones_de_practica(id_practica):
    cursor = mysql.connection.cursor()
    sql = """
        SELECT o.id_observacion, o.descripcion, o.fecha, e.nombre, e.apellido
        FROM observaciones o
        JOIN practicas p ON o.id_practica = p.id_practica
        JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
        WHERE o.id_practica = %s
    """
    cursor.execute(sql, (id_practica,))
    datos = cursor.fetchall()
    cursor.close()
    
    if not datos:
        return jsonify({"mensaje": "Esta práctica no cuenta con observaciones aún"}), 404
        
    observaciones = [{"id_observacion": f[0], "descripcion": f[1], "fecha": str(f[2]), "estudiante": f"{f[3]} {f[4]}"} for f in datos]
    return jsonify(observaciones), 200

@app.route('/instituciones/resumen_practicas', methods=['GET'])
def resumen_practicas_instituciones():
    cursor = mysql.connection.cursor()
    sql = """
        SELECT i.id_institucion, i.nombre, COUNT(p.id_practica) AS total_practicas, IFNULL(SUM(p.horas), 0) AS total_horas
        FROM instituciones i
        LEFT JOIN compras p ON i.id_institucion = p.id_institucion
        GROUP BY i.id_institucion, i.nombre
    """
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()
    
    resumen = [{"id_institucion": f[0], "institucion": f[1], "cantidad_practicas": f[2], "total_horas_acumuladas": int(f[3])} for f in datos]
    return jsonify(resumen), 200

if __name__ == "__main__":
    app.run(debug=True)