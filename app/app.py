from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from config import init_app
import os


# Inicializa la app
app = Flask(__name__)

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
    # Verifica si el archivo es válido y tiene una extensión permitida
    if file and allowed_file(file.filename):
        # Obtén el nombre seguro del archivo
        filename = secure_filename(file.filename)

        # Define la ruta donde se guardarán las fotos
        upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

        # Verifica si el directorio existe, si no, lo crea
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Guarda el archivo en el directorio 'uploads'
        file.save(os.path.join(upload_folder, filename))

        # Retorna el nombre del archivo guardado
        return filename
    return None  # Si el archivo no es válido o no existe

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
            return render_template('public/layout.html', msg='Debe cargar una foto', tipo=1)
        
        foto = request.files['foto']
        
        if foto.filename == '':
            return render_template('public/layout.html', msg='Debe seleccionar una foto para cargar', tipo=1)

        # Si el archivo es válido, guardarlo
        nuevoNombreFile = recibeFoto(foto)
        if nuevoNombreFile:
            # Aquí iría el código para registrar el juego en la base de datos (simulado por ahora)
            # resultData = registrarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, nuevoNombreFile)
            return render_template('public/layout.html', msg='El Registro fue un éxito', tipo=1)
        else:
            return render_template('public/layout.html', msg='Formato de archivo no permitido. Debe ser una imagen', tipo=1)
        
        

# Simulación de la función para registrar un juego (en tu caso aquí iría la lógica de la base de datos)
def registrarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto):
    # Aquí es donde registrarías el juego en tu base de datos.
    # Esto es solo una simulación de éxito.
    return 1

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

@app.errorhandler(404)
def notfound(error):
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(debug=True)