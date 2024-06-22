from flask import Flask, request
import psycopg2

import os
from dotenv import load_dotenv

from datetime import date

app = Flask(__name__)

load_dotenv()

mapa_doc = {
    "chilena": "Cédula Chilena",
    "mercosur": "Documento Mercosur",
    "pasaporte": "Pasaporte",
}


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    )
    return conn


@app.post("/cliente")
def cliente_post():
    try:
        nro_doc = request.form["nro_doc"]
        tipo_doc = request.form["tipo_doc"]
        nombre = request.form["nombre"]
        nacionalidad = request.form["nacionalidad"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
    except KeyError:
        app.logger.debug(request.form.keys())
        return (
            "<alert>No se pudo registrar el cliente, los datos ingresados son incorrectos.</alert>",
            400,
        )

    tipo_doc = mapa_doc[tipo_doc]

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT crear_cliente(%s, %s, %s, %s, %s, %s)",
            (nro_doc, tipo_doc, nombre, nacionalidad, correo, telefono),
        )
    except psycopg2.errors.UniqueViolation:
        return "<alert>El cliente ya existe</alert>", 400
    conn.commit()
    cur.close()
    conn.close()

    return "<alert>Se registró con éxito al cliente.</alert>"


@app.get("/cliente")
def cliente_get():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    app.logger.debug(f"{nro_doc} | {tipo_doc}")

    tipo_doc = mapa_doc.get(tipo_doc)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT servicios_usados(%s, %s)", (nro_doc, tipo_doc))
    servicios = cur.fetchall()
    cur.close()
    conn.close()
    return servicios


@app.post("/reserva")
def nueva_reserva():
    try:
        cant_personas = request.form["cant_personas"]
        nro_doc = request.form["nro_doc"]
        tipo_doc = request.form["tipo_doc"]
        id_servicio = request.form["servicio"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
    except KeyError:
        app.logger.debug(request.form.keys())
        return (
            "<alert>No se pudo registrar el cliente, los datos ingresados son incorrectos.</alert>",
            400,
        )

    tipo_doc = mapa_doc[tipo_doc]
    folio = request.form.get("folio")

    conn = get_db_connection()
    cur = conn.cursor()

    if folio is not None:
        cur.execute(
            "INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, folio, fecha_inicio, fecha_fin)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                cant_personas,
                nro_doc,
                tipo_doc,
                id_servicio,
                folio,
                fecha_inicio,
                fecha_fin,
            ),
        )
    else:
        cur.execute(
            "INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, fecha_inicio, fecha_fin)"
            "VALUES (%s, %s, %s, %s, %s, %s)"
            "RETURNING folio",
            (cant_personas, nro_doc, tipo_doc, id_servicio, fecha_inicio, fecha_fin),
        )

        folio = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return f"Se registró una nueva reserva con folio {folio}"


@app.get("/limpieza")
def limpieza_servicio():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    tipo_doc = mapa_doc.get(tipo_doc)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """SELECT id_servicio, nombre_servicio FROM servicioLimpiezaEmpleado
                WHERE nro_documento = %s AND tipo_documento =  %s;""",
        (nro_doc, tipo_doc),
    )
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

    cur.execute(
        """
                SELECT sueldo FROM sueldo
                WHERE nro_documento = %s AND tipo_documento = %s;
                """,
        (nro_doc, tipo_doc),
    )
    sueldo = cur.fetchone()[0]
    app.logger.debug(sueldo)

    cur.close()
    conn.close()
    return str(sueldo)


@app.get("/ingresos")
def ingresos_mes():
    fecha = request.args.get("fecha")
    if fecha is None:
        fecha = date.today()
        app.logger.debug(fecha)
    else:
        fecha = date.fromisoformat(fecha)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT monto FROM ingresos WHERE ano = %s AND mes = %s;",
        (fecha.year, fecha.month),
    )
    sueldo = cur.fetchone()[0]
    app.logger.debug(sueldo)

    cur.close()
    conn.close()
    return str(sueldo)


@app.get("/temporada")
def temporada_get():
    fecha = request.args.get("fecha")
    if fecha is None:
        fecha = date.today()
        app.logger.debug(fecha)
    else:
        fecha = date.fromisoformat(fecha)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
                SELECT * FROM Temporada
                WHERE fecha_inicio < %s AND fecha_fin > %s;
                """,
        (fecha, fecha),
    )

    datos_temporada = cur.fetchall()

    return datos_temporada


@app.post("/temporada")
def temporada_post():
    try:
        temporada = request.form["temporada"]
        fecha_inicio = date.fromisoformat(request.form["fecha_inicio"])
        fecha_fin = date.fromisoformat(request.form["fecha_fin"])
        lodge = request.form["lodge"]
        lodge_tinaja = request.form["lodge_tinaja"]
        cabana = request.form["cabana"]
        tinaja = request.form["tinaja"]
        quincho = request.form["quincho"]
    except KeyError:
        app.logger.debug(request.form.keys())
        return (
            "<alert>No se pudo registrar el cliente, los datos ingresados son incorrectos.</alert>",
            400,
        )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO Temporada (temporada, fecha_inicio, fecha_fin, valor_lodge, valor_lodge_tinaja, valor_cabana, valor_tinaja, valor_quincho)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            temporada,
            fecha_inicio,
            fecha_fin,
            lodge,
            lodge_tinaja,
            cabana,
            tinaja,
            quincho,
        ),
    )

    conn.commit()
    cur.close()
    conn.close()
    return f"Se crearon los datos para la temporada {temporada}"
