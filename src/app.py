from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Función para conectar a la base de datos MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),  # ruta de la base de datos
            database=os.getenv('DB_NAME'),  # nombre de la base de datos a usar
            user=os.getenv('DB_USER'),  # usuario de MySQL
            password=os.getenv('DB_PASS')  # contraseña de MySQL
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para registrar un trabajador
@app.route('/register_trabajador', methods=('GET', 'POST'))
def register_trabajador():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_ingreso = request.form['fecha_ingreso']
        tipo_trabajador = request.form['tipo_trabajador']
        finca = request.form['finca']
        eps = request.form['eps']
        fondo_pensiones = request.form['fondo_pensiones']
        fondo_cesantias = request.form['fondo_cesantias']
        salario = request.form['salario']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Trabajadores (cedula, nombres, apellidos, fecha_ingreso, tipo_trabajador, finca, eps, fondo_pensiones, fondo_cesantias, salario) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (cedula, nombres, apellidos, fecha_ingreso, tipo_trabajador, finca, eps, fondo_pensiones, fondo_cesantias, salario))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('trabajadores.html')

# Ruta para registrar una labor
@app.route('/register_labor', methods=('GET', 'POST'))
def register_labor():
    if request.method == 'POST':
        identificador = request.form['identificador']
        finca = request.form['finca']
        lote = request.form['lote']
        valor = request.form['valor']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Labores (identificador, finca, lote, valor) 
            VALUES (%s, %s, %s, %s)
        ''', (identificador, finca, lote, valor))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('labores.html')

# Ruta para registrar una relación trabajador-labor
@app.route('/register_trabajador_labor', methods=('GET', 'POST'))
def register_trabajador_labor():
    if request.method == 'POST':
        fecha = request.form['fecha']
        cantidad = request.form['cantidad']
        id_trabajador = request.form['id_trabajador']
        id_labor = request.form['id_labor']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Trabajador_labores (fecha, cantidad, id_trabajador, id_labor) 
            VALUES (%s, %s, %s, %s)
        ''', (fecha, cantidad, id_trabajador, id_labor))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('trabajador_labores.html')

# Ruta para consultar registros trabajador-labor
@app.route('/consultar_trabajador_labor', methods=('GET', 'POST'))
def consultar_trabajador_labor():
    registros = []
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        id_trabajador = request.form.get('id_trabajador')
        id_labor = request.form.get('id_labor')

        query = '''
            SELECT tl.fecha, t.nombres, t.apellidos, l.finca, l.lote, tl.cantidad 
            FROM Trabajador_labores tl
            JOIN Trabajadores t ON tl.id_trabajador = t.cedula
            JOIN Labores l ON tl.id_labor = l.identificador
            WHERE 1=1
        '''
        params = []

        if fecha:
            query += ' AND tl.fecha = %s'
            params.append(fecha)
        if id_trabajador:
            query += ' AND tl.id_trabajador = %s'
            params.append(id_trabajador)
        if id_labor:
            query += ' AND tl.id_labor = %s'
            params.append(id_labor)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('consultar_trabajador_labores.html', registros=registros)

# Ruta para consultar registros trabajador-labor en un rango de fechas
@app.route('/consultar_trabajador_labor_rango', methods=('GET', 'POST'))
def consultar_trabajador_labor_rango():
    registros = []
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        id_trabajador = request.form.get('id_trabajador')
        id_labor = request.form.get('id_labor')

        query = '''
            SELECT tl.fecha, t.nombres, t.apellidos, l.finca, l.lote, tl.cantidad, l.valor, (tl.cantidad * l.valor) as total 
            FROM Trabajador_labores tl
            JOIN Trabajadores t ON tl.id_trabajador = t.cedula
            JOIN Labores l ON tl.id_labor = l.identificador
            WHERE tl.fecha BETWEEN %s AND %s
        '''
        params = [fecha_inicio, fecha_fin]

        if id_trabajador:
            query += ' AND tl.id_trabajador = %s'
            params.append(id_trabajador)
        if id_labor:
            query += ' AND tl.id_labor = %s'
            params.append(id_labor)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('consultar_trabajador_labores_rango.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True)
