from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from config import init_app
import os
from flask_mysqldb import MySQL
# Asegúrate de importar SQLAlchemy


# Inicializa la app
app = Flask(__name__, template_folder='../app/templates/')

# Establecer una clave secreta única
app.config['SECRET_KEY'] = 'gamehub'

# Configura para que las plantillas se recarguen automáticamente
app.config['TEMPLATES_AUTO_RELOAD'] = True



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '38150362Kiara'
app.config['MYSQL_DB'] = 'fernandez_oller_luppi_kener'

mysql = init_app(app)

msg = ''
tipo = ''

# Rutas
@app.route('/', methods=['GET', 'POST'])
def inicio():
    from controller.controllerJuego import listaJuegos  # Importa aquí para evitar el ciclo
    return render_template('public/layout.html', miData=listaJuegos())

# Configuración para la carga de archivos
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directorio donde se guardarán las imágenes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar el tamaño máximo a 16 MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Tipos de archivo permitidos

# Verifica si el archivo tiene una extensión permitida
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Ajusta las extensiones permitidas según lo necesites
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def recibeFoto(file):
    if file and allowed_file(file.filename):  # Asegúrate de que el archivo sea válido
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

        # Verificar si el directorio existe, si no, lo crea
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Guardar la foto en el directorio 'uploads'
        file.save(os.path.join(upload_folder, filename))

        # Retorna el nombre del archivo
        return filename
    return None


@app.route('/registrar-juego', methods=['GET', 'POST'])
def addJuego():
    return render_template('public/acciones/add.html')

@app.route('/juego', methods=['POST'])
def formAddJuego():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        anio_lanzamiento = request.form['anio_lanzamiento']
        plataforma = request.form['plataforma']
        disponibilidad = request.form['disponibilidad']

        # Verificar si se ha cargado un archivo
        if 'foto' not in request.files:
            flash('Debe cargar una foto', 'error')
            return redirect(url_for('addJuego'))

        foto = request.files['foto']
        
        if foto.filename == '':
            flash('Debe seleccionar una foto para cargar', 'error')
            return redirect(url_for('addJuego'))

        # Si el archivo es válido, guardarlo
        nuevoNombreFile = recibeFoto(foto)
        if nuevoNombreFile:
            # Registrar el juego en la base de datos
            resultData = registrarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, nuevoNombreFile)
            if resultData == 1:
                flash('El juego se ha registrado exitosamente', 'success')
                return redirect(url_for('inicio'))  # Redirigir a la página principal
            else:
                flash('Error al registrar el juego', 'error')
                return redirect(url_for('addJuego'))
        else:
            flash('Formato de archivo no permitido. Debe ser una imagen', 'error')
            return redirect(url_for('addJuego'))

# Simulación de la función para registrar un juego (aquí iría la lógica de la base de datos)
def registrarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto):
    cur = mysql.connection.cursor()
    try:
        cur.execute('''INSERT INTO juegos (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                    (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto))
        mysql.connection.commit()
        return 1  # Éxito
    except Exception as e:
        mysql.connection.rollback()  # Revertir cambios si hay un error
        return 0  # Error


#Ruta para eliminar un juego
@app.route('/borrar-juego', methods=['POST'])
def formViewBorrarJuego():
    if request.method == 'POST':
        # Obtener los datos enviados desde el frontend
        idJuego = request.form['id']
        nombreFoto = request.form['nombreFoto']

        # Llamar a la función que elimina el juego y la foto
        resultData = eliminarJuego(idJuego, nombreFoto)

        if resultData == 1:
            return jsonify([1])  # Respuesta exitosa
        else:
            return jsonify([0])  # Error al eliminar


def eliminarJuego(idJuego='', nombreFoto=''):
    cur = mysql.connection.cursor()

    # Eliminar el juego de la base de datos
    cur.execute('DELETE FROM juegos WHERE id=%s', (idJuego,))
    mysql.connection.commit()
    resultadoeliminar = cur.rowcount

    # Eliminar la foto asociada al juego
    basepath = os.path.dirname(__file__)
    url_File = os.path.join(basepath, 'static', 'assets', 'fotos_juegos', nombreFoto)

    if os.path.exists(url_File):
        os.remove(url_File)

    return resultadoeliminar  # Si se eliminó correctamente, devuelve 1, si no 0



@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editarJuego(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM juegos WHERE id = %s', (id,))
    juego = cur.fetchone()

    if not juego:
        return "Juego no encontrado", 404

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        anio_lanzamiento = request.form['anio_lanzamiento']
        plataforma = request.form['plataforma']
        disponibilidad = request.form['disponibilidad']

        print(f"Datos recibidos: {nombre}, {categoria}, {descripcion}, {precio}, {anio_lanzamiento}, {plataforma}, {disponibilidad}")

        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                nuevoNombreFile = recibeFoto(foto)
            else:
                nuevoNombreFile = juego['foto']
        else:
            nuevoNombreFile = juego['foto']

        result = actualizarJuego(id, nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, nuevoNombreFile)

        if result == 1:
            return redirect(url_for('inicio'))
        else:
            return render_template('public/layout.html', msg='Error al actualizar el juego', tipo=1)

    return render_template('public/acciones/update.html', juego=juego)


def actualizarJuego(id, nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, nuevoNombreFile):
    cur = mysql.connection.cursor()
    query = """
    UPDATE juegos
    SET nombre = %s, categoria = %s, descripcion = %s, precio = %s, anio_lanzamiento = %s, plataforma = %s, disponibilidad = %s, foto = %s
    WHERE id = %s
    """
    values = (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, nuevoNombreFile, id)
    print(f"Ejecutando query: {query} con valores {values}")  # Imprime la consulta para verificar
    cur.execute(query, values)
    mysql.connection.commit()

    if cur.rowcount == 1:  # Si se actualizó una fila
        return 1
    else:
        return 0



@app.route('/ver_juego/<int:id>', methods=['GET'])
def verJuego(id):
    # Usa la función `obtener_juego_por_id` para obtener los detalles del juego
    juego = obtener_juego_por_id(id)

    # Si no existe el juego, devuelve un mensaje de error
    if not juego:
        return "Juego no encontrado", 404

    # Renderiza la plantilla y pasa `juego` como `infoJuego`
    return render_template('public/acciones/view.html', infoJuego=juego)

def obtener_juego_por_id(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, categoria, foto, anio_lanzamiento, plataforma, precio FROM juegos WHERE id = %s", (id,))
    juego = cur.fetchone()
    cur.close()  # Asegúrate de cerrar el cursor

    if juego:
        # Convierte el resultado en un diccionario
        return {
            'id': juego[0],
            'nombre': juego[1],
            'categoria': juego[2],
            'foto': juego[3],
            'year': juego[4],
            'plataforma': juego[5],
            'precio': juego[6]
        }
    return None


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)