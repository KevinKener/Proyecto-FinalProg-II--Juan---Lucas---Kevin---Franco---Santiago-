#clases importadas
from flask import Flask, render_template, redirect, url_for

#Inicializa la app
app=Flask(__name__)

#metodo para indicar que esta es la ruta raiz
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    
    return redirect(url_for('index')) #metodo vinculado para la redireccion a la pagina principal

@app.route('/Login')
def login():
    return render_template("Login.html")

@app.route('/Carrito')
def Carrito():
    return render_template("carrito.html")

def pagina_no_encontrada(error):
    return render_template('404.html'),404
    
#condicion que comprueba si estamos en la app(la lanza)
if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)#debug en true para hacer las modificaciones en tiempo real