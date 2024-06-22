#!/bin/env python

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()

cur.execute('DROP SCHEMA public CASCADE')
cur.execute('CREATE SCHEMA public;')

cur.execute('CREATE TABLE IF NOT EXISTS Cliente(nro_documento VARCHAR(40),'
    'tipo_documento VARCHAR(20),'
    'nombre VARCHAR(100),'
    'nacionalidad VARCHAR(100),'
    'correo VARCHAR(50),'
    'telefono VARCHAR(25),'
    'PRIMARY KEY (nro_documento, tipo_documento),'
    'CONSTRAINT tipo_de_documento_valido CHECK (tipo_documento IN (\'Cédula Chilena\', \'Documento Mercosur\', \'Pasaporte\')));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Factura(folio SERIAL PRIMARY KEY,'
    'valor INT CHECK (valor >= 0),'
    'fecha DATE,'
    'estado VARCHAR(10),'
    'CONSTRAINT estado_pago CHECK(estado IN (\'PAGADO\', \'NO PAGADO\')));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Servicio(id_servicio INT PRIMARY KEY,'
    'nombre VARCHAR(100),'
    'capacidad INT,'
    'tipo_servicio VARCHAR(30),'
    'CONSTRAINT servicios_disponibles CHECK(tipo_servicio IN (\'QUINCHO\', \'TINAJA\', \'HOSPEDAJE\')));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Reserva(id_reserva SERIAL PRIMARY KEY,'
    'cant_personas INT CHECK (cant_personas >= 1),'
    'nro_documento_cliente VARCHAR(40),'
    'tipo_documento_cliente VARCHAR(20),'
    'id_servicio INT,'
    'folio INT,'
    'fecha_inicio DATE,'
    'fecha_fin DATE,'
    'FOREIGN KEY (nro_documento_cliente, tipo_documento_cliente) REFERENCES Cliente(nro_documento, tipo_documento), '
    'FOREIGN KEY (folio) REFERENCES Factura(folio),'
    'FOREIGN KEY (id_servicio) REFERENCES Servicio(id_servicio));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Hospedaje(id_servicio INT PRIMARY KEY,'
    'cant_camas_dobles INT,'
    'cant_camas_single INT,'
    'FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Cabana(id_servicio INT PRIMARY KEY,'
    'cant_habitaciones INT,'
    'FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Lodge(id_servicio INT PRIMARY KEY,'
    'con_tinaja CHAR(3),'
    'FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio),'
    'CONSTRAINT opcion_con_tinaja_valida CHECK (con_tinaja IN (\'SIN\',\'CON\')));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Empleado(nro_documento VARCHAR(40),'
    'tipo_documento VARCHAR(20),'
    'nombre VARCHAR(100),'
    'correo VARCHAR(50),'
    'telefono VARCHAR(25),'
    'sueldo INT,'
    'PRIMARY KEY(nro_documento, tipo_documento),'
    'CONSTRAINT tipo_de_documento_valido CHECK (tipo_documento IN (\'Cédula Chilena\', \'Documento Mercosur\', \'Pasaporte\')));'
)

cur.execute('CREATE TABLE IF NOT EXISTS PersonalLimpieza(nro_documento VARCHAR(40),'
    'tipo_documento VARCHAR(20),'
    'PRIMARY KEY(nro_documento, tipo_documento),'
    'FOREIGN KEY(nro_documento, tipo_documento) REFERENCES Empleado(nro_documento, tipo_documento));'
)

cur.execute('CREATE TABLE IF NOT EXISTS LimpiezaServicio(nro_documento VARCHAR(40),'
    'tipo_documento VARCHAR(20),'
    'id_servicio INT,'
    'PRIMARY KEY (nro_documento, tipo_documento, id_servicio),'
    'FOREIGN KEY (nro_documento, tipo_documento) REFERENCES PersonalLimpieza(nro_documento, tipo_documento),'
    'FOREIGN KEY (id_servicio) REFERENCES Servicio(id_servicio));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Temporada('
    'temporada VARCHAR(20) PRIMARY KEY,'
    'fecha_inicio DATE,'
    'fecha_fin DATE,'
    'valor_lodge INTEGER CHECK (valor_lodge > 0),'
    'valor_lodge_tinaja INTEGER CHECK (valor_lodge_tinaja > 0),'
    'valor_cabana INTEGER CHECK (valor_cabana > 0),'
    'valor_tinaja INTEGER CHECK (valor_tinaja > 0),'
    'valor_quincho INTEGER CHECK (valor_quincho > 0));'
)

cur.execute('CREATE TABLE IF NOT EXISTS Contacto(id_contacto SERIAL PRIMARY KEY,'
    'nombre TEXT,'
    'telefono VARCHAR(25),'
    'descripcion TEXT);'
)

cur.execute('CREATE TABLE IF NOT EXISTS PersonalAdministrativo(nro_documento VARCHAR(40),'
    'tipo_documento VARCHAR(20),'
    'PRIMARY KEY (nro_documento, tipo_documento), '
    'FOREIGN KEY (nro_documento, tipo_documento) REFERENCES Empleado(nro_documento, tipo_documento));'
)

cur.execute('CREATE TABLE IF NOT EXISTS AdministrativoContacto(id_contacto INTEGER,'
    'nro_doc_empleado VARCHAR(40),'
    'tipo_doc_empleado VARCHAR(20),'
    'PRIMARY KEY (id_contacto, nro_doc_empleado, tipo_doc_empleado),'
    'FOREIGN KEY (id_contacto) REFERENCES Contacto(id_contacto),'
    'FOREIGN KEY (nro_doc_empleado, tipo_doc_empleado) REFERENCES PersonalAdministrativo(nro_documento, tipo_documento));'
)


cur.execute("""
            CREATE OR REPLACE FUNCTION crear_cliente(new_nro_documento VARCHAR(40), new_tipo_documento VARCHAR(20), new_nombre VARCHAR(100), new_nacionalidad VARCHAR(100), new_correo VARCHAR(50), new_telefono VARCHAR(25))
            RETURNS VOID AS $$
            BEGIN
                INSERT INTO Cliente(nro_documento, tipo_documento, nombre, nacionalidad, correo, telefono)
                VALUES(new_nro_documento, new_tipo_documento, new_nombre, new_nacionalidad, new_correo, new_telefono);
            END
            $$ LANGUAGE plpgsql;
            """)

cur.execute("""
            CREATE OR REPLACE FUNCTION verificar_reserva()
            RETURNS TRIGGER AS $$
            BEGIN
                IF (NEW.fecha_inicio = OLD.fecha_inicio) AND (NEW.fecha_fin = OLD.fecha_fin)
                THEN
                    RETURN NEW;
                END IF;
            
            	IF (
            		SELECT COUNT(*)
            		FROM reserva
            		WHERE (NEW.fecha_inicio >= reserva.fecha_inicio) AND 
            		(NEW.fecha_fin <= reserva.fecha_fin) AND (NEW.id_servicio = reserva.id_servicio) 
            	) != 0
            	THEN
            		RAISE EXCEPTION 'Ya hay una reserva entre esas fechas';
            	END IF;

            	RETURN NEW;
            END
            $$ LANGUAGE plpgsql;

            CREATE OR REPLACE TRIGGER verificar_reserva
            BEFORE INSERT ON reserva
            FOR EACH ROW
            EXECUTE PROCEDURE verificar_reserva();
            """)

cur.execute("""
            CREATE OR REPLACE VIEW valorServicio AS
            SELECT temp.temporada, s.id_servicio, temp.valor_cabana as valor FROM Cabana s CROSS JOIN Temporada temp
            UNION ALL SELECT temp.temporada, s.id_servicio, temp.valor_lodge as valor FROM Lodge s CROSS JOIN Temporada temp WHERE s.con_tinaja = 'SIN'
            UNION ALL SELECT temp.temporada, s.id_servicio, temp.valor_lodge_tinaja as valor FROM Lodge s CROSS JOIN Temporada temp WHERE s.con_tinaja = 'CON'
            UNION ALL SELECT temp.temporada, s.id_servicio, temp.valor_tinaja as valor FROM Servicio s CROSS JOIN Temporada temp WHERE s.tipo_servicio = 'TINAJA'
            UNION ALL SELECT temp.temporada, s.id_servicio, temp.valor_quincho as valor FROM Servicio s CROSS JOIN Temporada temp WHERE s.tipo_servicio = 'QUINCHO';
            """)

# TODO: Multiplicar precio por cantidad de noches
cur.execute("""
            CREATE OR REPLACE FUNCTION actualizar_factura()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.folio IS NULL
                THEN
                    WITH folio AS (
                        WITH temp AS (
                            SELECT * FROM valorServicio
                            WHERE temporada = (SELECT temporada FROM Temporada WHERE fecha_inicio < NEW.fecha_inicio AND fecha_fin > NEW.fecha_inicio)
                            AND id_servicio = NEW.id_servicio
                        )
                        INSERT INTO Factura(valor, fecha, estado)
                        SELECT t.valor, NEW.fecha_fin, 'NO PAGADO'
                        FROM temp as t
                        RETURNING folio
                    ) SELECT * INTO NEW.folio FROM folio;
                ELSE
                    WITH temp AS (
                        SELECT * FROM valorServicio
                        WHERE temporada = (SELECT temporada FROM Temporada WHERE fecha_inicio < NEW.fecha_inicio AND fecha_fin > NEW.fecha_inicio)
                        AND id_servicio = NEW.id_servicio
                    )
                    UPDATE Factura f SET valor = f.valor + t.valor
                    FROM temp as t
                    WHERE folio = NEW.folio;
                END IF;
            
                RETURN NEW;
            END
            $$ LANGUAGE plpgsql;

            CREATE OR REPLACE TRIGGER actualizar_factura
            BEFORE INSERT ON Reserva
            FOR EACH ROW
            EXECUTE PROCEDURE actualizar_factura();
            """)

cur.execute("""
            CREATE OR REPLACE VIEW sueldo AS
                SELECT nombre, nro_documento, tipo_documento, sueldo
                FROM Empleado;
            """)

cur.execute("""
            CREATE OR REPLACE VIEW servicioLimpiezaEmpleado AS
            SELECT s.id_servicio as id_servicio,
                s.nombre as nombre_servicio,
                e.nombre as nombre_empleado,
                e.nro_documento as nro_documento,
                e.tipo_documento as tipo_documento
            FROM LimpiezaServicio ls
            INNER JOIN Empleado e USING (nro_documento, tipo_documento)
            INNER JOIN Servicio s USING (id_servicio);
            """)

cur.execute("""
            CREATE OR REPLACE VIEW preciosTemporada AS
            SELECT * FROM Temporada
                WHERE fecha_inicio < NOW()
                AND fecha_fin > NOW();
            """)

cur.execute("""
            CREATE OR REPLACE VIEW ingresos AS
            SELECT EXTRACT(YEAR FROM f.fecha) as ano,
                EXTRACT(MONTH FROM f.fecha) as mes,
                SUM(f.valor) as monto
            FROM factura f GROUP BY ano, mes;
            """)

cur.execute("""
            CREATE OR REPLACE FUNCTION disponibilidad_servicio(inicio DATE, fin DATE, servicio_nombre VARCHAR(1000))
            RETURNS TABLE (servicio VARCHAR(100) , folio_RET INT) AS $$
            BEGIN
                RETURN QUERY 
            	SELECT servicio.nombre, folio 
            	FROM reserva
            	INNER JOIN servicio on reserva.id_servicio = servicio.id_servicio
            	WHERE (inicio >= fecha_inicio) AND (fin <= fecha_fin) AND (servicio.nombre = servicio_nombre);
            END;
            $$ LANGUAGE plpgsql;
            """)

#TODO: Pasar a una view
cur.execute("""
            CREATE OR REPLACE FUNCTION servicios_usados(nro_documento VARCHAR(40), tipo_documento VARCHAR(20))
            RETURNS TABLE (folio INT, valor INT, nombre VARCHAR(100)) AS $$
            BEGIN
                RETURN QUERY 
                SELECT Factura.folio, Factura.valor ,servicio.nombre
            	FROM Reserva INNER JOIN Factura
            	ON Reserva.folio = Factura.folio
            	INNER JOIN servicio ON servicio.id_servicio = reserva.id_servicio
            	WHERE (Reserva.nro_documento_cliente = nro_documento) AND (Reserva.tipo_documento_cliente = tipo_documento);
            END;
            $$ LANGUAGE plpgsql;
            """)

cur.execute("""
            INSERT INTO Temporada(temporada, fecha_inicio, fecha_fin, valor_lodge,
                valor_lodge_tinaja, valor_cabana, valor_tinaja, valor_quincho)
            VALUES
                ('Otoño 2024', '2024-03-15', '2024-06-30', 45000, 60000, 75000, 40000, 60000),
                ('Invierno 2024', '2024-06-30', '2024-08-15', 65000, 80000, 140000, 40000, 60000);
            """)

cur.execute("""
            INSERT INTO Servicio (id_servicio, nombre, capacidad, tipo_servicio)
            VALUES
                (101, 'Refugio del Sol', 5, 'HOSPEDAJE'),
	            (102, 'Refugio del Agua', 5, 'HOSPEDAJE'),
	            (103, 'Refugio del Bosque', 5, 'HOSPEDAJE'),
	            (104, 'Refugio de la Tierra', 5, 'HOSPEDAJE'),

	            (201, 'Habitación 1', 2, 'HOSPEDAJE'),
	            (202, 'Habitación 2', 2, 'HOSPEDAJE'),
	            (203, 'Habitación 3', 2, 'HOSPEDAJE'),
	            (204, 'Habitación 4', 2, 'HOSPEDAJE'),
	            (205, 'Habitación 5', 2, 'HOSPEDAJE'),
	            (206, 'Habitación 6', 2, 'HOSPEDAJE'),
	            (207, 'Habitación 7', 2, 'HOSPEDAJE'),

	            (800, 'Tinaja', 6, 'TINAJA'),
	            (900, 'Quincho', 20, 'QUINCHO');
            """)

cur.execute("""
            INSERT INTO Hospedaje (id_servicio, cant_camas_dobles, cant_camas_single)
            VALUES
            	(101, 1, 4),
            	(102, 1, 4),
            	(103, 1, 4),
            	(104, 1, 4),

            	(201, 1, 0),
            	(202, 1, 0),
            	(203, 1, 0),
            	(204, 1, 0),
            	(205, 1, 0),
            	(206, 1, 0),
            	(207, 1, 0);
            """)

cur.execute("""
            INSERT INTO Cabana (id_servicio, cant_habitaciones)
            VALUES
            	(101, 2),
                (102, 2),
                (103, 2),
                (104, 2);
            """)

cur.execute("""
            INSERT INTO Lodge (id_servicio, con_tinaja)
            VALUES
            	(201, 'SIN'),
                (202, 'SIN'),
                (203, 'SIN'),
                (204, 'SIN'),
                (205, 'SIN'),
                (206, 'SIN'),
                (207, 'CON');
            """)

cur.execute("""
            INSERT INTO Cliente (nro_documento, tipo_documento, nombre, nacionalidad, correo, telefono)
            VALUES 
                ('12345678', 'Cédula Chilena', 'Ana Gomez', 'Chilena', 'ana_gomez@gmail.com', '12345678'),
                ('87654321', 'Documento Mercosur', 'Carlos Mendez', 'Argentina', 'carlos_mendez@gmail.com', '87654321'),
                ('A1234567', 'Pasaporte', 'Beatriz Fernández', 'Peruana', 'beatriz_fernandez@gmail.com', '98765432'),
                ('22334455', 'Cédula Chilena', 'Roberto Silva', 'Chilena', 'roberto_silva@gmail.com', '22334455'),
                ('55667788', 'Documento Mercosur', 'Mariana Lopez', 'Brasilera', 'mariana_lopez@gmail.com', '55667788'),
                ('B7654321', 'Pasaporte', 'Jorge Martínez', 'Uruguaya', 'jorge_martinez@gmail.com', '11223344'),
                ('33445566', 'Cédula Chilena', 'Sofía Rodríguez', 'Chilena', 'sofia_rodriguez@gmail.com', '33445566'),
                ('66778899', 'Documento Mercosur', 'Lucas Gonzales', 'Paraguaya', 'lucas_gonzales@gmail.com', '66778899'),
                ('C9876543', 'Pasaporte', 'Valentina Herrera', 'Boliviana', 'valentina_herrera@gmail.com', '99887766');
            """)

cur.execute("""
            INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, fecha_inicio, fecha_fin)
            VALUES
                (2, 'B7654321', 'Pasaporte', 207, '2024-05-12', '2024-05-18'),
                (4, '33445566', 'Cédula Chilena', 104, '2024-05-10', '2024-05-13'),
                (5, '12345678', 'Cédula Chilena', 102, '2024-05-10', '2024-05-13');
            ;
            """)

cur.execute("""
            INSERT INTO Reserva (cant_personas, nro_documento_cliente, tipo_documento_cliente, id_servicio, folio, fecha_inicio, fecha_fin)
            VALUES
                (5, '12345678', 'Cédula Chilena', 800, 3, '2024-05-10', '2024-05-10');
            """)

cur.execute("""
            INSERT INTO Empleado (nro_documento, tipo_documento, nombre, correo, telefono, sueldo)
            VALUES
                ('49785432', 'Cédula Chilena', 'Rosa María Lama', 'rosamaria@gmail.com', '789654123', 2000000),
                ('94706789', 'Cédula Chilena', 'Victor Zúñiga', 'vzuniga@gmail.com', '988467801', 500000),
                ('A7940349', 'Documento Mercosur', 'Fernando Flores', 'fernanflo@gmail.com', '978060489', 1500000),
                ('97064907', 'Pasaporte', 'Carmen Rozas', 'carmencita@gmail.com', '970690768', 300000);
            """)

cur.execute("""
            INSERT INTO PersonalLimpieza (nro_documento, tipo_documento)
            VALUES
                ('94706789', 'Cédula Chilena'),
                ('97064907', 'Pasaporte');
            """)

cur.execute("""
            INSERT INTO PersonalAdministrativo (nro_documento, tipo_documento)
            VALUES
                ('49785432', 'Cédula Chilena'),
                ('A7940349', 'Documento Mercosur');
            """)

cur.execute("""
            INSERT INTO LimpiezaServicio (nro_documento, tipo_documento, id_servicio)
            VALUES
                ('94706789', 'Cédula Chilena', 101),
                ('94706789', 'Cédula Chilena', 800),
                ('94706789', 'Cédula Chilena', 206),
                ('97064907', 'Pasaporte', 900),
                ('97064907', 'Pasaporte', 103),
                ('97064907', 'Pasaporte', 102);
            """)

conn.commit()
cur.close()
conn.close()
