from flask import Flask, jsonify, request, render_template,session
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "una_clave_secreta_mucho_mas_larga_y_segura_para_el_proyecto_2026"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "practicas_db"
#app.config['MYSQL_PORT'] = 3306

#
CORS(app)
mysql = MySQL(app)
jwt = JWTManager(app) 

@app.route('/')
def inicio():
    #return f"<h2>Servidor Flask en ejecucion :)</h2>"
    #return render_template('index.html')
    #return render_template('login.html')
    return render_template('login.html')

@app.route('/testdb')
def test():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1")
    cursor.close()
    return "¡Conexión a la Base de Datos exitosa!"




#Estudiantes
@app.route("/estudiantes/listar")
def estudiantes_listar():
    return render_template("estudiantes/listar.html")

@app.route("/estudiantes/nuevo")
def estudiantes_nuevo():
    return render_template("estudiantes/añadirEstudiante.html")

@app.route('/estudiantes/editar/<int:id_estudiante>')
def editar_estudiante(id_estudiante):
    return render_template("estudiantes/form.html",id_estudiante=id_estudiante)

@app.route('/estudiantes/form/<int:id>')
@jwt_required()
def formulario_estudiante(id):
    return render_template(
        'estudiantes/form.html',
        id=id
    )

#INSTITUCIONES
@app.route("/instituciones/listar")
def instituciones_listar():
    return render_template("instituciones/listar.html")

@app.route("/instituciones/nuevo")
def instituciones_nuevo():
    return render_template("instituciones/anadirInstitucion.html")

@app.route('/instituciones/editar/<int:id_institucion>')
def editar_institucion(id_institucion):

    return render_template(
        "instituciones/form.html",
        id_institucion=id_institucion
    )

#PRÁCTICAS
@app.route("/practicas/listar")
def practicas_listar():
    return render_template("practicas/listar.html")

@app.route("/practicas/nuevo")
def practicas_nuevo():
    return render_template("practicas/anadirPractica.html")

@app.route('/practicas/editar/<int:id_practica>')
def editar_practica(id_practica):

    return render_template(
        "practicas/form.html",
        id_practica=id_practica
    )

#OBSERVACIONES
@app.route("/observaciones/listar")
def observaciones_listar():
    return render_template("observaciones/listar.html")

@app.route("/observaciones/nuevo")
def observaciones_nuevo():
    return render_template("observaciones/anadirObservacion.html") 

@app.route('/observaciones/editar/<int:id_observacion>')
def editarObservacion(id_observacion):

    return render_template(
        "observaciones/form.html",
        id_observacion=id_observacion
    )
#-------------------------------------------------------

@app.route('/base')
def base_html():
    return render_template('base.html')
    #return render_template('dashboard.html')


@app.route('/dashboard_')
def dashboard_html():
    return render_template('dashboard.html')

@app.route('/dashboard', methods=['GET'])
#@jwt_required()
def dashboard():

    cursor = mysql.connection.cursor()

    # Total estudiantes
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    estudiantes = cursor.fetchone()[0]

    # Total instituciones
    cursor.execute("SELECT COUNT(*) FROM instituciones")
    instituciones = cursor.fetchone()[0]

    # Total prácticas
    cursor.execute("SELECT COUNT(*) FROM practicas")
    practicas = cursor.fetchone()[0]

    # Total observaciones
    cursor.execute("SELECT COUNT(*) FROM observaciones")
    observaciones = cursor.fetchone()[0]

    cursor.close()

    return jsonify({
        "estudiantes": estudiantes,
        "instituciones": instituciones,
        "practicas": practicas,
        "observaciones": observaciones
    })
#-------------------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == '12345':
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
        
    return jsonify({"error": "Credenciales incorrectas"}), 401

#ESTUDIANTES
#===========================================================
# LISTAR ESTUDIANTES
@app.route('/estudiantes', methods=['GET'])
#@jwt_required()
def listar_estudiantes():

    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM estudiantes"

    cursor.execute(sql)

    datos = cursor.fetchall()

    estudiantes = []

    for fila in datos:
        estudiantes.append({
            'id_estudiante': fila[0],
            'nombre': fila[1],
            'apellido': fila[2],
            'carrera': fila[3],
            'correo': fila[4],
            'telefono': fila[5]
        })

    cursor.close()
    return jsonify(estudiantes)


# INSERTAR ESTUDIANTE
@app.route('/estudiantes', methods=['POST'])
#@jwt_required()
def insertar_estudiante():

    data = request.get_json()

    nombre = data['nombre']
    apellido = data['apellido']
    carrera = data['carrera']
    correo = data['correo']
    telefono = data['telefono']

    cursor = mysql.connection.cursor()

    sql = """
        INSERT INTO estudiantes
        (nombre, apellido, carrera, correo, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nombre, apellido, carrera, correo, telefono))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Estudiante registrado correctamente'
    })


# OBTENER ESTUDIANTE POR ID
@app.route('/estudiantes/<int:id>', methods=['GET'])
@jwt_required()
def obtener_estudiante(id):

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM estudiantes WHERE id_estudiante = %s"

    cursor.execute(sql, (id,))
    dato = cursor.fetchone()

    cursor.close()

    if dato is None:
        return jsonify({
            'mensaje': 'Estudiante no encontrado'
        }), 404

    estudiante = {
        'id_estudiante': dato[0],
        'nombre': dato[1],
        'apellido': dato[2],
        'carrera': dato[3],
        'correo': dato[4],
        'telefono': dato[5]
    }

    return jsonify(estudiante)


# MODIFICAR ESTUDIANTE
@app.route('/estudiantes/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_estudiante(id):

    data = request.get_json()

    nombre = data['nombre']
    apellido = data['apellido']
    carrera = data['carrera']
    correo = data['correo']
    telefono = data['telefono']

    cursor = mysql.connection.cursor()

    sql = """
        UPDATE estudiantes
        SET nombre = %s,
            apellido = %s,
            carrera = %s,
            correo = %s,
            telefono = %s
        WHERE id_estudiante = %s
    """

    cursor.execute(
        sql,
        (nombre, apellido, carrera, correo, telefono, id)
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Estudiante modificado correctamente'
    })


# ELIMINAR ESTUDIANTE
@app.route('/estudiantes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_estudiante(id):

    cursor = mysql.connection.cursor()

    sql = "DELETE FROM estudiantes WHERE id_estudiante = %s"

    cursor.execute(sql, (id,))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Estudiante eliminado correctamente'
    })
#=============================================================

#============================================================
#INSTITUCIONES
# LISTAR INSTITUCIONES
@app.route('/instituciones', methods=['GET'])
#@jwt_required()
def listar_instituciones():

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM instituciones"

    cursor.execute(sql)

    datos = cursor.fetchall()

    instituciones = []

    for fila in datos:
        instituciones.append({
            'id_institucion': fila[0],
            'nombre': fila[1],
            'direccion': fila[2],
            'telefono': fila[3],
            'responsable': fila[4]
        })

    cursor.close()

    return jsonify(instituciones)


# INSERTAR INSTITUCION
@app.route('/instituciones', methods=['POST'])
@jwt_required()
def insertar_institucion():

    data = request.get_json()

    nombre = data['nombre']
    direccion = data['direccion']
    telefono = data['telefono']
    responsable = data['responsable']

    cursor = mysql.connection.cursor()

    sql = """
        INSERT INTO instituciones
        (nombre, direccion, telefono, responsable)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (nombre, direccion, telefono, responsable)
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Institución registrada correctamente'
    })


# OBTENER INSTITUCION POR ID
@app.route('/instituciones/<int:id>', methods=['GET'])
@jwt_required()
def obtener_institucion(id):

    cursor = mysql.connection.cursor()

    sql = """
        SELECT * FROM instituciones
        WHERE id_institucion = %s
    """

    cursor.execute(sql, (id,))

    dato = cursor.fetchone()

    cursor.close()

    if dato is None:

        return jsonify({
            'mensaje': 'Institución no encontrada'
        }), 404

    institucion = {
        'id_institucion': dato[0],
        'nombre': dato[1],
        'direccion': dato[2],
        'telefono': dato[3],
        'responsable': dato[4]
    }

    return jsonify(institucion)


# MODIFICAR INSTITUCION
@app.route('/instituciones/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_institucion(id):

    data = request.get_json()

    nombre = data['nombre']
    direccion = data['direccion']
    telefono = data['telefono']
    responsable = data['responsable']

    cursor = mysql.connection.cursor()

    sql = """
        UPDATE instituciones
        SET nombre = %s,
            direccion = %s,
            telefono = %s,
            responsable = %s
        WHERE id_institucion = %s
    """

    cursor.execute(
        sql,
        (nombre, direccion, telefono, responsable, id)
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Institución modificada correctamente'
    })


# ELIMINAR INSTITUCION
@app.route('/instituciones/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_institucion(id):

    cursor = mysql.connection.cursor()

    sql = """
        DELETE FROM instituciones
        WHERE id_institucion = %s
    """

    cursor.execute(sql, (id,))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Institución eliminada correctamente'
    })

#===========================================================
#PRACTICAS

# LISTAR PRACTICAS
@app.route('/practicas', methods=['GET'])
@jwt_required()
def listar_practicas():

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM practicas"

    cursor.execute(sql)

    datos = cursor.fetchall()

    practicas = []

    for fila in datos:
        practicas.append({
            'id_practica': fila[0],
            'id_estudiante': fila[1],
            'id_institucion': fila[2],
            'fecha_inicio': str(fila[3]),
            'fecha_fin': str(fila[4]),
            'horas': fila[5],
            'estado': fila[6]
        })

    cursor.close()

    return jsonify(practicas)


# INSERTAR PRACTICA
@app.route('/practicas', methods=['POST'])
@jwt_required()
def insertar_practica():

    data = request.get_json()

    id_estudiante = data['id_estudiante']
    id_institucion = data['id_institucion']
    fecha_inicio = data['fecha_inicio']
    fecha_fin = data['fecha_fin']
    horas = data['horas']
    estado = data['estado']

    cursor = mysql.connection.cursor()

    sql = """
        INSERT INTO practicas
        (id_estudiante, id_institucion, fecha_inicio, fecha_fin, horas, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            id_estudiante,
            id_institucion,
            fecha_inicio,
            fecha_fin,
            horas,
            estado
        )
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Práctica registrada correctamente'
    })


# OBTENER PRACTICA POR ID
@app.route('/practicas/<int:id>', methods=['GET'])
@jwt_required()
def obtener_practica(id):

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM practicas WHERE id_practica = %s"

    cursor.execute(sql, (id,))

    dato = cursor.fetchone()

    cursor.close()

    if dato is None:

        return jsonify({
            'mensaje': 'Práctica no encontrada'
        }), 404

    practica = {
        'id_practica': dato[0],
        'id_estudiante': dato[1],
        'id_institucion': dato[2],
        'fecha_inicio': str(dato[3]),
        'fecha_fin': str(dato[4]),
        'horas': dato[5],
        'estado': dato[6]
    }

    return jsonify(practica)


# MODIFICAR PRACTICA
@app.route('/practicas/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_practica(id):

    data = request.get_json()

    id_estudiante = data['id_estudiante']
    id_institucion = data['id_institucion']
    fecha_inicio = data['fecha_inicio']
    fecha_fin = data['fecha_fin']
    horas = data['horas']
    estado = data['estado']

    cursor = mysql.connection.cursor()

    sql = """
        UPDATE practicas
        SET id_estudiante = %s,
            id_institucion = %s,
            fecha_inicio = %s,
            fecha_fin = %s,
            horas = %s,
            estado = %s
        WHERE id_practica = %s
    """

    cursor.execute(
        sql,
        (
            id_estudiante,
            id_institucion,
            fecha_inicio,
            fecha_fin,
            horas,
            estado,
            id
        )
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Práctica modificada correctamente'
    })


# ELIMINAR PRACTICA
@app.route('/practicas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_practica(id):

    cursor = mysql.connection.cursor()

    sql = "DELETE FROM practicas WHERE id_practica = %s"

    cursor.execute(sql, (id,))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Práctica eliminada correctamente'
    })
#============================================================
#
#OBSERVACIONES
#============================================================
# LISTAR OBSERVACIONES
@app.route('/observaciones', methods=['GET'])
@jwt_required()
def listar_observaciones():

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM observaciones"

    cursor.execute(sql)

    datos = cursor.fetchall()

    observaciones = []

    for fila in datos:
        observaciones.append({
            'id_observacion': fila[0],
            'id_practica': fila[1],
            'descripcion': fila[2],
            'fecha': str(fila[3])
        })

    cursor.close()

    return jsonify(observaciones)


# INSERTAR OBSERVACION
@app.route('/observaciones', methods=['POST'])
@jwt_required()
def insertar_observacion():

    data = request.get_json()

    id_practica = data['id_practica']
    descripcion = data['descripcion']
    fecha = data['fecha']

    cursor = mysql.connection.cursor()

    sql = """
        INSERT INTO observaciones
        (id_practica, descripcion, fecha)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        sql,
        (id_practica, descripcion, fecha)
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Observación registrada correctamente'
    })


# OBTENER OBSERVACION POR ID
@app.route('/observaciones/<int:id>', methods=['GET'])
@jwt_required()
def obtener_observacion(id):

    cursor = mysql.connection.cursor()

    sql = """
        SELECT * FROM observaciones
        WHERE id_observacion = %s
    """

    cursor.execute(sql, (id,))

    dato = cursor.fetchone()

    cursor.close()

    if dato is None:

        return jsonify({
            'mensaje': 'Observación no encontrada'
        }), 404

    observacion = {
        'id_observacion': dato[0],
        'id_practica': dato[1],
        'descripcion': dato[2],
        'fecha': str(dato[3])
    }

    return jsonify(observacion)


# MODIFICAR OBSERVACION
@app.route('/observaciones/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_observacion(id):

    data = request.get_json()

    id_practica = data['id_practica']
    descripcion = data['descripcion']
    fecha = data['fecha']

    cursor = mysql.connection.cursor()

    sql = """
        UPDATE observaciones
        SET id_practica = %s,
            descripcion = %s,
            fecha = %s
        WHERE id_observacion = %s
    """

    cursor.execute(
        sql,
        (
            id_practica,
            descripcion,
            fecha,
            id
        )
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Observación modificada correctamente'
    })


# ELIMINAR OBSERVACION
@app.route('/observaciones/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_observacion(id):

    cursor = mysql.connection.cursor()

    sql = """
        DELETE FROM observaciones
        WHERE id_observacion = %s
    """

    cursor.execute(sql, (id,))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Observación eliminada correctamente'
    })


#===============================================================

#obtener las prácticas de un estudiante específico.
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

#Obtener todas las observaciones asociadas a una práctica específica.
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

#genera un resumen de prácticas por institución.
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