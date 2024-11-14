from config import mysql  # Importa la instancia de MySQL desde config.py
import random
import string

# controller/controllerJuego.py

from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

def agregarJuego():
    # Verifica si el formulario fue enviado con una foto
    if 'foto' not in request.files:
        flash('No se ha seleccionado una foto', 'error')
        return redirect(url_for('add_juego'))  # Redirigir a la página de agregar juego

    foto = request.files['foto']
    
    # Verificar si el archivo tiene una extensión válida
    if foto and allowed_file(foto.filename):
        # Asegúrate de que el nombre del archivo sea seguro
        filename = secure_filename(foto.filename)
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Guardar la foto en la carpeta uploads
        foto.save(foto_path)

        # Obtener el nombre del juego desde el formulario
        nombre = request.form['nombre']
        
        # Insertar el juego en la base de datos
        try:
            cur = app.mysql.connection.cursor()
            cur.execute('''INSERT INTO juegos (nombre, foto) VALUES (%s, %s)''', (nombre, filename))
            app.mysql.connection.commit()  # Confirmar los cambios
            cur.close()

            flash('Juego agregado con éxito', 'success')
        except Exception as e:
            flash(f'Ocurrió un error al agregar el juego: {str(e)}', 'error')
            app.mysql.connection.rollback()  # Hacer rollback si hubo un error
        return redirect(url_for('lista'))  # Redirigir a la lista de juegos

    else:
        flash('Archivo no permitido o no seleccionado', 'error')
        return redirect(url_for('add_juego'))


def listaJuegos():
    # Crea el cursor para ejecutar la consulta
    cur = mysql.connection.cursor()

    # Modifica la consulta para incluir las columnas 'categoria' y 'anio_lanzamiento'
    cur.execute('SELECT id, nombre, categoria, anio_lanzamiento, foto FROM juegos')

    # Obtiene todos los registros
    juegos = cur.fetchall()

    # Convertir la lista de tuplas a una lista de diccionarios
    juegos_dict = []
    for juego in juegos:
        juego_dict = {
            'id': juego[0],
            'nombre': juego[1],
            'categoria': juego[2],  # Añade la categoría
            'anio_lanzamiento': juego[3],  # Añade el año de lanzamiento
            'foto': juego[4]  # Foto
        }
        juegos_dict.append(juego_dict)

    return juegos_dict


def registrarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto):
    cur = mysql.connection.cursor()

    cur.execute('''INSERT INTO juegos (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto))

    mysql.connection.commit()
    cur.close()

    return 1  # Registro exitoso


def detallesdelJuego(idJuego):
    cur = mysql.connection.cursor(dictionary=True)
    cur.execute('SELECT * FROM juegos WHERE id = %s', (idJuego,))
    juego = cur.fetchone()
    cur.close()

    return juego


def actualizarJuego(idJuego, nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto):
    cur = mysql.connection.cursor()

    # Obtener el nombre de la foto actual si no se proporciona una nueva
    if foto:
        cur.execute('''UPDATE juegos SET nombre = %s, categoria = %s, descripcion = %s, precio = %s, anio_lanzamiento = %s, 
                       plataforma = %s, disponibilidad = %s, foto = %s WHERE id = %s''',
                    (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto, idJuego))
    else:
        # Aquí obtienes el nombre de la foto actual antes de la actualización
        cur.execute('''SELECT foto FROM juegos WHERE id = %s''', (idJuego,))
        juego = cur.fetchone()
        foto_actual = juego['foto'] if juego else None

        cur.execute('''UPDATE juegos SET nombre = %s, categoria = %s, descripcion = %s, precio = %s, anio_lanzamiento = %s, 
                       plataforma = %s, disponibilidad = %s, foto = %s WHERE id = %s''',
                    (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto_actual, idJuego))

    mysql.connection.commit()
    cur.close()
    return 1  # Actualización exitosa


def stringAleatorio():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))