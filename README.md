📚 Little Bookshelf

Proyecto ASIR2 · Flask + MySQL

Aplicación web desarrollada con Flask que permite gestionar libros y reseñas.
Incluye registro de personas usuarias, sistema de autenticación, búsqueda de libros, creación de reviews y visualización de rankings editoriales.

🚀 Tecnologías utilizadas

Python 3.12

Flask

MySQL / MariaDB

HTML5 + CSS3

Jinja2

📦 Instalación y ejecución en local
1️⃣ Clonar el repositorio
git clone https://github.com/TU-USUARIO/TU-REPO.git
cd TU-REPO
2️⃣ Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

En Windows:

.venv\Scripts\activate
3️⃣ Instalar dependencias
pip install -r requirements.txt
4️⃣ Configurar la base de datos

Accede a MySQL o MariaDB:

mysql -u root -p

Ejecuta el script de creación:

SOURCE schema.sql;

Esto creará:

Base de datos projecte_myrna

Tablas users, books, reviews

Datos iniciales de prueba

5️⃣ Configurar conexión en db.py

Verifica que los datos de conexión coincidan con tu entorno:

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TU_PASSWORD",
        database="projecte_myrna"
    )

Modifica usuario y contraseña según tu configuración local.

6️⃣ Ejecutar la aplicación
python app.py

La aplicación se ejecutará en:

http://127.0.0.1:5000
👤 Usuarios de prueba

Incluidos en el schema.sql:

Usuario	Contraseña
admin	123456
luna	123456
nico	123456
vera	123456
eric	123456
iris	123456
bruno	123456
noa	123456
alex	123456
sara	123456
marc	123456
📂 Estructura del proyecto
.
├── app.py
├── db.py
├── schema.sql
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── search.html
│   ├── profile.html
│   └── ...
└── static/
    ├── style.css
    └── uploads/
✨ Funcionalidades principales

Registro e inicio de sesión

Perfil con historial de reseñas

Búsqueda por título o autor

Listado alfabético A–Z de libros

Top 10 editorial dinámico

Subida de imágenes locales

Sistema de reviews con puntuación 1–5

Eliminación de reviews propias

🧹 Archivos excluidos del repositorio

El proyecto no incluye:

.venv

__pycache__

Archivos temporales del sistema

🔮 Posibles mejoras futuras

Sistema de edición de libros

Panel administrador

Filtros avanzados por género y año

Paginación en búsquedas

Sistema de valoraciones agregadas

Despliegue en entorno cloud

📜 Licencia

Proyecto académico desarrollado para ASIR2. Uso educativo.
