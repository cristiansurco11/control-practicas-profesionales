# Sistema de Control de Prácticas Profesionales

## Descripción del proyecto

Sistema web desarrollado para la gestión y control de prácticas profesionales.  
Permite administrar la información de estudiantes, instituciones, prácticas profesionales y observaciones relacionadas con el seguimiento de las actividades realizadas.

El sistema fue desarrollado utilizando Flask como framework backend, MySQL como gestor de base de datos y plantillas HTML para la interfaz de usuario.

---

# Tecnologías utilizadas

- Python 3
- Flask
- MySQL
- Flask-MySQLdb
- Flask-JWT-Extended
- PyJWT
- HTML
- CSS
- JavaScript

---

# Requisitos previos

Para ejecutar correctamente el proyecto se necesita tener instalado:

- Python 3.x
- MySQL Server
- pip (gestor de paquetes de Python)

---

# Instalación del proyecto

Clonar el repositorio:

```bash
git clone https://github.com/cristiansurco11/control-practicas-profesionales.git
```

Ingresar a la carpeta del proyecto:

```bash
cd control-practicas-profesionales
```

---

# Instalación de dependencias

Crear un entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

# Configuración de la base de datos

El sistema utiliza MySQL para almacenar la información del sistema.

Crear la base de datos:

```sql
CREATE DATABASE practicas_db;
```

Después se deben configurar los datos de conexión en el archivo principal del proyecto:

```python
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "practicas_db"
```

La base de datos contiene las tablas principales:

- estudiantes
- instituciones
- practicas
- observaciones

---

# Ejecución de migraciones

Este proyecto no utiliza Flask-Migrate.

La estructura de la base de datos debe ser creada directamente en MySQL mediante las tablas necesarias para el funcionamiento del sistema.

---

# Ejecución del servidor

Activar primero el entorno virtual y ejecutar:

```bash
python app.py
```

El servidor estará disponible en:

```
http://127.0.0.1:5000
```

---

# Estructura del proyecto

```
control-practicas-profesionales/

│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── estudiantes/
│   ├── instituciones/
│   ├── practicas/
│   └── observaciones/
│
├── static/
│
```

---

# Funcionalidades principales

## Gestión de estudiantes

Permite:

- Registrar estudiantes.
- Consultar estudiantes registrados.
- Editar información de estudiantes.

## Gestión de instituciones

Permite:

- Registrar instituciones.
- Consultar instituciones registradas.
- Actualizar información.

## Gestión de prácticas profesionales

Permite:

- Registrar prácticas profesionales.
- Asociar estudiantes con instituciones.
- Consultar y modificar prácticas.

## Gestión de observaciones

Permite:

- Registrar observaciones.
- Realizar seguimiento del desarrollo de las prácticas.

---

# API y Endpoints

El sistema cuenta con endpoints desarrollados utilizando Flask, los cuales permiten la comunicación entre la aplicación y la base de datos.

Los endpoints utilizan diferentes métodos HTTP:

- GET: permite consultar información.
- POST: permite registrar nuevos datos.
- PUT: permite actualizar información existente.

Estos endpoints funcionan como intermediarios entre la interfaz del sistema y la base de datos, permitiendo gestionar estudiantes, instituciones, prácticas y observaciones.

---

# Autenticación

El sistema implementa autenticación mediante JWT (JSON Web Token), permitiendo controlar el acceso a determinadas funcionalidades y proteger las rutas que requieren autorización.

---

# Autor

Proyecto desarrollado como sistema de gestión de prácticas profesionales.