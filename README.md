# Little Bookshelf
**Proyecto ASIR2 · Flask + MySQL**

Aplicación web desarrollada con Flask que permite gestionar libros y reseñas. 
Incluye registro de personas usuarias, sistema de autenticación, búsqueda de libros, creación de reviews y visualización de rankings editoriales.

## Tecnologías utilizadas
* Python 3.12
* Flask
* MySQL / MariaDB
* HTML5 + CSS3
* Jinja2

## Instalación y ejecución en local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU-USUARIO/TU-REPO.git](https://github.com/TU-USUARIO/TU-REPO.git) && cd TU-REPO
```
* `git clone`: Descarga el código fuente del repositorio especificado a tu máquina local.
* `cd`: Cambia el directorio de trabajo actual a la carpeta del proyecto recién clonado.

### 2. Crear entorno virtual
```bash
python3 -m venv .venv && source .venv/bin/activate
```
* `python3 -m venv`: Crea un entorno virtual aislado en la carpeta especificada para manejar las dependencias del proyecto sin afectar al sistema global.
* `source`: Lee y ejecuta el script de activación en la shell actual, habilitando el entorno virtual.

En Windows:
```cmd
python -m venv .venv && .venv\Scripts\activate
```
* `python -m venv`: Equivalente en Windows para crear el entorno.
* `.venv\Scripts\activate`: Ejecutable que activa el entorno virtual en la terminal de Windows.

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
* `pip install -r`: Lee el archivo de texto especificado y descarga e instala todas las librerías y versiones listadas en él.

### 4. Configurar la base de datos
```bash
mysql -u root -p < schema.sql
```
* `mysql`: Llama al cliente de línea de comandos del gestor de base de datos.
* `-u root`: Especifica que te conectas con el usuario administrador.
* `-p`: Indica al sistema que solicite la contraseña de forma segura.
* `< schema.sql`: Redirige el contenido del archivo SQL como entrada al comando, ejecutando su contenido (creación de base de datos, tablas e inserción de datos iniciales).

### 5. Configurar conexión en db.py
Verifica que los datos de conexión coincidan con tu entorno:
```python
def get_connection(): return mysql.connector.connect(host="localhost", user="root", password="TU_PASSWORD", database="projecte_myrna")
```
Modifica usuario y contraseña según tu configuración local.

### 6. Ejecutar la aplicación
```bash
python app.py
```
* `python`: Llama al intérprete para ejecutar el script principal, el cual inicia el servidor web de desarrollo de Flask.

La aplicación se ejecutará en: `http://127.0.0.1:5000`


Como entrar a la db en GUI:
sudo service mariadb status
sudo service mariadb start
sudo ss -lntp | grep 3306
sudo mysql
CREATE USER 'gui'@'localhost' IDENTIFIED BY 'UnaPasswordFuerte';
GRANT ALL PRIVILEGES ON projecte_myrna.* TO 'gui'@'localhost';
FLUSH PRIVILEGES; 

o 

CREATE USER 'gui'@'%' IDENTIFIED BY 'UnaPasswordFuerte';
GRANT ALL PRIVILEGES ON projecte_myrna.* TO 'gui'@'%';
FLUSH PRIVILEGES;

Si aun así no conecta: revisa bind-address
En WSL, abre:

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
Si aun así no conecta: revisa bind-address
En WSL, abre:

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf

sudo apt update
sudo apt install -y php php-mysqli
mkdir -p ~/adminer && cd ~/adminer
wget https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1.php -O index.php
php -S 0.0.0.0:8080
http://localhost:8080

