from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import init_app
import os

# Inicializa la app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AuronPlay69'
app.config['MYSQL_DB'] = 'fernandez_oller_luppi_kener'

mysql = init_app(app)

msg = ''
tipo = ''

# Rutas
@app.route('/', methods=['GET', 'POST'])
def inicio():
    from controller.controllerJuego import listaJuegos  # Importa aquí para evitar el ciclo
    return render_template('public/layout.html', miData=listaJuegos())

@app.route('/registrar-juego', methods=['GET', 'POST'])
def addJuego():
    return render_template('public/acciones/add.html')

@app.route('/juego', methods=['POST'])
def formAddJuego():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        anio_lanzamiento = request.form['anio_lanzamiento']
        plataforma = request.form['plataforma']
        disponibilidad = request.form['disponibilidad']

        if request.files['foto']:
            file = request.files['foto']
            nuevoNombreFile = recibeFoto(file)
            from controller.controllerJuego import registrarJuego  # Importa aquí para evitar el ciclo
            resultData = registrarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, nuevoNombreFile)
            if resultData == 1:
                return render_template('public/layout.html', miData=listaJuegos(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg='Método HTTP incorrecto', tipo=1)
        else:
            return render_template('public/layout.html', msg='Debe cargar una foto', tipo=1)

#Ruta para eliminar un juego
@app.route('/borrar-juego', methods=['POST'])
def formViewBorrarJuego():
    if request.method == 'POST':
        # Obtener los datos enviados desde el frontend
        idJuego = request.form['id']
        nombreFoto = request.form['nombreFoto']

        resultData = eliminarJuego(idJuego, nombreFoto)

        if resultData == 1:
            return jsonify([1])  # Respuesta exitosa
        else:
            return jsonify([0])  # Error al eliminar

#Función para eliminar un juego y su foto
def eliminarJuego(idJuego='', nombreFoto=''):
    cur = mysql.connection.cursor()

    # Eliminar el juego de la base de datos
    cur.execute('DELETE FROM juegos WHERE id=%s', (idJuego,))
    mysql.connection.commit()
    resultadoeliminar = cur.rowcount

    # Eliminar la foto asociada al juego
    basepath = os.path.dirname(file)  # Corregido: usar _file (doble guion bajo)
    url_File = os.path.join(basepath, 'static', 'assets', 'fotos_juegos', nombreFoto)

    if os.path.exists(url_File):
        os.remove(url_File)

    return resultado_eliminar  # Si se eliminó correctamente, devuelve 1, si no 0

def recibeFoto(file):
    basepath = os.path.dirname(__file__)
    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1]
    nuevoNombreFile = stringAleatorio() + extension

    upload_path = os.path.join(basepath, 'static/assets/fotos_juegos', nuevoNombreFile)
    file.save(upload_path)

    return nuevoNombreFile

@app.errorhandler(404)
def notfound(error):
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(debug=True)