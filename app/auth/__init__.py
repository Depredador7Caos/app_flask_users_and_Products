from flask import Blueprint, render_template, redirect, url_for, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

athentication = Blueprint("loading", __name__, template_folder = "templates")
mysql = MySQL()

#ZONA DE RUTAS
@athentication.route("/")
def index():
    return render_template("index.html")


@athentication.route("/lista")
def users_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    usuarios = cur.fetchall()
    cur.close()

    return render_template('contactos/lista_contactos.html', list_user = usuarios)


#------------- PARTE DE LOGEO ---------------
@athentication.route('/admin')
def administrador():
    return render_template('logeo/admin.html')


@athentication.route('/cliente')
def cliente():
    return render_template('logeo/cliente.html')


@athentication.route("/register-new-user")
def register_user():
    return render_template("logeo/_new-user.html")


@athentication.route('/sing-in')
def atraer_login():
    return render_template('logeo/formulario.html')


@athentication.route("/nuevo-usuario", methods=['GET', 'POST'])
def new_user():
    firstName = request.form['txtFirstName']
    lastName = request.form['txtLastName']
    numberPhone = request.form['txtNumber']
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (firstName, lastName, email, phone, password, id_rol) VALUES (%s, %s, %s, %s, %s, 2)",(firstName, lastName, correo, numberPhone, password))

    mysql.connection.commit()

    return render_template('logeo/formulario.html')


@athentication.route('/acceso-login', methods=['GET','POST'])
def acceso():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
        _correo = request.form["txtCorreo"]
        _password = request.form["txtPassword"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email= %s AND password= %s", (_correo, _password))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']

            if session['id_rol'] == 1:
                return render_template("logeo/admin.html")
            elif session['id_rol'] == 2:
                return render_template("logeo/cliente.html")
        else:
            return render_template('logeo/formulario.html', message ="Ususario no encontrado")


#------------- PARTE PRODUCTOS --------------
@athentication.route('/build-product')
def create_product():
    return render_template('productos/_build_product.html', message="Producto agregado correctamente")


@athentication.route('/lista_productos')
def get_product():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()

    return render_template('productos/_list_product.html', list_product = productos)


@athentication.route("/product_add", methods=['GET', 'POST'])
def add_product():
    nombreProducto = request.form['nombre_producto']
    imageProducto = request.form['image_producto']
    precioProducto = request.form['precio_producto']
    categoriaProducto = request.form['categoria_producto']
    cantidadProducto = request.form['cantidad_producto']
    fechaEntrada = request.form['entrada']
    fechaSalida = request.form['salida']
    fechaCaducidad = request.form['caducidad']
    horaCaducidad = request.form['hora_caducidad']
    descripcionProducto = request.form['descripcion_producto']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO productos (nombre, cantidad, precio, url_img, categoria, descripcion, fecha_entrada, fecha_salida, fecha_caducidad, hora_caducidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (nombreProducto, cantidadProducto, precioProducto, imageProducto, categoriaProducto, descripcionProducto, fechaEntrada, fechaSalida, fechaCaducidad, horaCaducidad))

    mysql.connection.commit()

    return render_template("productos/_build_product.html")
