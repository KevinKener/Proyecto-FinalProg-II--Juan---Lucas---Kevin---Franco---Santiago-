from config import mysql  # Importa la instancia de MySQL desde config.py
import random
import string


def listaJuegos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre, foto FROM juegos')  # Asegúrate de seleccionar la columna foto
    juegos = cur.fetchall()

    # Convertir la lista de tuplas a una lista de diccionarios
    juegos_dict = []
    for juego in juegos:
        juego_dict = {
            'id': juego[0],
            'nombre': juego[1],
            'foto': juego[2]
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


def recibeActualizarJuego(nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto, idJuego):
    cur = mysql.connection.cursor()

    cur.execute('''UPDATE juegos SET nombre = %s, categoria = %s, descripcion = %s, precio = %s, anio_lanzamiento = %s, 
                   plataforma = %s, disponibilidad = %s, foto = %s WHERE id = %s''',
                (nombre, categoria, descripcion, precio, anio_lanzamiento, plataforma, disponibilidad, foto, idJuego))

    mysql.connection.commit()
    cur.close()

    return 1  # Actualización exitosa


def stringAleatorio():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))