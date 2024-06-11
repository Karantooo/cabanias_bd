CREATE TABLE cliente(
	nro_documento VARCHAR(40),
	tipo_documento VARCHAR(20),
	nombre VARCHAR(100),
	nacionalidad VARCHAR(100),
	correo VARCHAR(50),
	telefono VARCHAR(25),
	
	PRIMARY KEY (nro_documento, tipo_documento),
	CONSTRAINT tipo_de_documento_valido CHECK (tipo_documento IN ('Cédula Chilena', 'Documento Mercosur', 'Pasaporte'))
	
);


CREATE TABLE reserva(
	id_reserva INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	cant_personas INT,
	nro_documento_cliente VARCHAR(40),
	tipo_documento_cliente VARCHAR(20),
	id_servicio INT,
	folio INT,
	fecha_inicio DATE,
	fecha_fin DATE,


	FOREIGN KEY (nro_documento_cliente, tipo_documento_cliente) REFERENCES cliente(nro_documento, tipo_documento), 
	FOREIGN KEY (folio) REFERENCES factura(folio),
	FOREIGN KEY (id_servicio) REFERENCES servicio(id_servicio) 
);

CREATE TABLE factura(
	folio INT PRIMARY KEY,
	valor INT,
	fecha DATE,
	estado VARCHAR(10),

	CONSTRAINT estado_pago CHECK(estado IN ('PAGADO', 'NO PAGADO'))
);

CREATE TABLE servicio(
	id_servicio INT PRIMARY KEY,
	nombre VARCHAR(100),
	capacidad INT,
	tipo_servicio VARCHAR(30),

	CONSTRAINT servicios_disponibles CHECK(tipo_servicio IN ('QUINCHO', 'TINAJA', 'HOSPEDAJE'))
);
