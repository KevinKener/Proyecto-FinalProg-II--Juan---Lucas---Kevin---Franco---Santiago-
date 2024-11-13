from flask import Flask, render_template, redirect, url_for

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    
    return redirect(url_for('index'))

@app.route('/Login')
def login():
    return render_template("Login.html")

@app.route('/Carrito')
def Carrito():
    return render_template("carrito.html")

def pagina_no_encontrada(error):
    return render_template('404.html'),404
    

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)