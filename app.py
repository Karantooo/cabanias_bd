from flask import Flask, request, render_template, flash, url_for, redirect
import psycopg2

import os
from dotenv import load_dotenv

import json
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

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


@app.route("/")
def index():
    return render_template("index.html")


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
            "No se pudo registrar el cliente, los datos ingresados son incorrectos.",
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
        return "El cliente ya existe", 400
    conn.commit()
    cur.close()
    conn.close()

    return "Se registró con éxito al cliente."


@app.get("/cliente")
def cliente_get():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    app.logger.debug(f"{nro_doc} | {tipo_doc}")

    tipo_doc = mapa_doc.get(tipo_doc)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
SELECT row_to_json(t)
FROM (
  SELECT nro_documento, tipo_documento,
    (
      SELECT array_to_json(array_agg(row_to_json(r)))
      FROM (
        SELECT folio, valor, servicio
        FROM serviciosCliente
        WHERE nro_documento = c.nro_documento AND tipo_documento = c.tipo_documento
        ORDER BY folio
      ) r
    ) as reservas
  FROM Cliente c
  WHERE nro_documento = %s AND tipo_documento = %s
) t
        """,
        (nro_doc, tipo_doc),
    )

    servicios = cur.fetchone()
    ret_servicios = json.dumps(servicios[0])

    cur.close()
    conn.close()
    return ret_servicios


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
            "No se pudo registrar el cliente, los datos ingresados son incorrectos.",
            400,
        )

    tipo_doc = mapa_doc[tipo_doc]
    folio = request.form.get("folio")

    conn = get_db_connection()
    cur = conn.cursor()

    if folio is not None:
        cur.execute(
            """
INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, folio, fecha_inicio, fecha_fin)
VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
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
            """
INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, fecha_inicio, fecha_fin)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING folio
            """,
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
        """
SELECT row_to_json(t)
FROM (
  SELECT nombre, nro_documento, tipo_documento,
    (
      SELECT json_array (
        SELECT nombre_servicio
        FROM servicioLimpiezaEmpleado
        WHERE nro_documento = e.nro_documento AND tipo_documento = e.tipo_documento
      )
    ) as servicios
  FROM Empleado e
  WHERE nro_documento = %s AND tipo_documento = %s
) t
        """,
        (nro_doc, tipo_doc),
    )

    servicios = cur.fetchone()
    ret_servicios = json.dumps(servicios[0])

    cur.close()
    conn.close()
    return ret_servicios


@app.get("/sueldo")
def sueldo_empleado():
    nro_doc = request.args.get("nro_doc")
    tipo_doc = request.args.get("tipo_doc")

    tipo_doc = mapa_doc.get(tipo_doc)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
SELECT row_to_json(s) FROM Sueldo s
WHERE nro_documento = %s AND tipo_documento = %s;
        """,
        (nro_doc, tipo_doc),
    )

    sueldo = cur.fetchone()
    ret_sueldo = json.dumps(sueldo[0])

    cur.close()
    conn.close()
    return ret_sueldo


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

    ingresos = cur.fetchone()[0]
    ret_ingresos = json.dumps({"mes": fecha.strftime("%b %Y"), "ingresos": ingresos})

    cur.close()
    conn.close()
    return ret_ingresos


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
SELECT row_to_json(t)
FROM (
  SELECT temporada, valor_lodge, valor_lodge_tinaja, valor_cabana, valor_tinaja, valor_quincho
  FROM Temporada WHERE fecha_inicio < %s AND fecha_fin > %s
) t;
        """,
        (fecha, fecha),
    )

    temporada = cur.fetchone()
    ret_temporada = json.dumps(temporada[0])

    cur.close()
    conn.close()
    return ret_temporada


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
            "No se pudo registrar el cliente, los datos ingresados son incorrectos.",
            400,
        )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
INSERT INTO Temporada (temporada, fecha_inicio, fecha_fin, valor_lodge, valor_lodge_tinaja, valor_cabana, valor_tinaja, valor_quincho)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
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

    flash(f"Se crearon los datos para la temporada {temporada}")
    return redirect(url_for("index"))
