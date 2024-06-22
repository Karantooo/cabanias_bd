from flask import Flask, request
import psycopg2

import os
from dotenv import load_dotenv

from datetime import date

app = Flask(__name__)

load_dotenv()

mapa_doc = {"chilena": "Cédula Chilena",
            "mercosur": "Documento Mercosur",
            "pasaporte": "Pasaporte"}

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='cabanas',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.post("/cliente")
def cliente_post():
    try:
        nro_doc = request.form['nro_doc']
        tipo_doc = request.form['tipo_doc']
        nombre = request.form['nombre']
        nacionalidad = request.form['nacionalidad']
        correo = request.form['correo']
        telefono = request.form['telefono']
    except KeyError:
        app.logger.debug(request.form.keys())
        return '<alert>No se pudo registrar el cliente, los datos ingresados son incorrectos.</alert>', 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT crear_cliente(%s, %s, %s, %s, %s, %s)',
                    (nro_doc, tipo_doc, nombre, nacionalidad, correo, telefono))
    except psycopg2.errors.UniqueViolation:
        return '<alert>El cliente ya existe</alert>', 400
    conn.commit()
    cur.close()
    conn.close()

    return '<alert>Se registró con éxito al cliente.</alert>'

@app.get("/cliente")
def cliente_get():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    app.logger.debug(f"{nro_doc} | {tipo_doc}")

    tipo_doc = mapa_doc.get(tipo_doc)


    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT servicios_usados(%s, %s)',
                (nro_doc, tipo_doc))
    servicios = cur.fetchall()
    cur.close()
    conn.close()
    return servicios

@app.post("/reserva")
def nueva_reserva():
    try:
        cant_personas = request.form['cant_personas']
        nro_doc = request.form['nro_doc']
        tipo_doc = request.form['tipo_doc']
        id_servicio = request.form['servicio']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
    except KeyError:
        app.logger.debug(request.form.keys())
        return '<alert>No se pudo registrar el cliente, los datos ingresados son incorrectos.</alert>', 400

    tipo_doc = mapa_doc[tipo_doc]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('INSERT INTO Factura (valor, fecha, estado)'
                'VALUES (%s, %s, %s)'
                'RETURNING folio',
                (0, fecha_fin, "NO PAGADO"))
    folio = cur.fetchall()
    cur.execute('INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, folio, fecha_inicio, fecha_fin)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (
                    cant_personas,
                    nro_doc,
                    tipo_doc,
                    id_servicio,
                    folio,
                    fecha_inicio,
                    fecha_fin
                ))

    conn.commit()
    cur.close()
    conn.close()
    return 'Se registró una nueva reserva'

@app.get("/limpieza")
def limpieza_servicio():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    tipo_doc = mapa_doc.get(tipo_doc)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT servicio_limpieza_empleado(%s, %s);',
                (nro_doc, tipo_doc))
    servicios = cur.fetchall()

    cur.close()
    conn.close()
    return servicios

@app.get("/sueldo")
def sueldo_empleado():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    tipo_doc = mapa_doc.get(tipo_doc)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT sueldo_empleado(%s, %s);',
                (nro_doc, tipo_doc))
    sueldo = cur.fetchall()
    app.logger.debug(sueldo)

    cur.close()
    conn.close()
    return sueldo

@app.get("/ingresos")
def ingresos_mes():
    fecha = request.args.get("fecha")
    if fecha is None:
        fecha = str(date.today())
        app.logger.debug(fecha)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT ingresos_mes(%s);',
                (fecha,))
    sueldo = cur.fetchall()
    app.logger.debug(sueldo)

    cur.close()
    conn.close()
    return sueldo