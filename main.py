from flask import Flask
from app.auth import *
from flask_mysqldb import MySQL, MySQLdb


app = Flask(__name__)

app.secret_key = "SECRET_KEY"

#----Propiedades para la conexion a base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'W3.rehog'
app.config['MYSQL_DB'] = 'python'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


#llamado de las rutas con uso de Blueprint
app.register_blueprint(athentication)

if __name__ == "__main__":
    app.run(
        debug = True
    )
