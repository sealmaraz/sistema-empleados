from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app=Flask (__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='empleados'

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql="SELECT * FROM empleados;"
    cursor.execute(sql)
    
    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/index.html',empleados=empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtnombre']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtFoto']

    now =datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto= tiempo +'_'+ _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)


    sql="INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
