from flask import render_template, request, redirect,send_from_directory, Flask, url_for
from flaskext.mysql import MySQL
from datetime import datetime
import os

app=Flask (__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='empleados'

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS #guardamos la ruta con un valor en la apps
mysql.init_app(app)

@app.route('/fotodeusuario/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('UPLOADS'), nombreFoto)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index():

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
        _foto.save("src/uploads/" + nuevoNombreFoto)


    sql="INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):

    sql="SELECT foto FROM empleados WHERE id=(%s)"
    datos=(id)
    cursor.execute(sql, datos)

    nombreFoto= cursor.fetchone()[0]

    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
    except:
        pass

    sql="DELETE FROM empleados WHERE id=(%s)"
    datos=(id)

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql="SELECT * FROM empleados WHERE id=(%s)"
    datos=(id)
    cursor.execute(sql, datos)
    empleado=cursor.fetchone()
    conn.commit()

    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtnombre']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    # datos=(_nombre, _correo, id)

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)
    
        sql = "SELECT foto FROM empleados WHERE id=(%s)"
        datos=(id)
        cursor.execute(sql, datos)
        conn.commit()
        
        nombreFoto=cursor.fetchone()[0]

        borrarEstaFoto = os.path.join(app.config['UPLOADS'], nombreFoto)
        
        
        try:
            os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
        except:
            pass

        sql="UPDATE empleados SET foto=(%s) WHERE id=(%s)"
        datos=(nuevoNombreFoto,id)
        cursor.execute(sql, datos)
        conn.commit()
    
    sql = "UPDATE empleados SET nombre=(%s), correo=(%s) WHERE id=(%s)"
    datos=(_nombre, _correo, id)
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)