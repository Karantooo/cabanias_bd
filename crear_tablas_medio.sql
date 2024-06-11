CREATE TABLE IF NOT EXISTS Hospedaje{
	id_servicio INT PRIMARY KEY,
	cant_camas_dobles INT,
	cant_camas_single INT,
	
	CONSTRAINT fk_id_servicio FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio)
};

CREATE TABLE IF NOT EXISTS Cabana{
	id_servicio INT PRIMARY KEY,
	cant_habitaciones INT,
	
	CONSTRAINT fk_id_servicio FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio)
};

CREATE TABLE IF NOT EXISTS Lodge{
	id_servicio INT PRIMARY KEY,
	con_tinaja CHAR(3),

	CONSTRAINT fk_id_servicio FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio),
	CONSTRAINT opcion_con_tinaja_valida CHECK(con_tinaja IN ('SIN','CON'))
};

CREATE TABLE IF NOT EXISTS Empleado{
	nro_documento VARCHAR(40),
	tipo_documento VARCHAR(20),
	nombre VARCHAR(100),
	correo VARCHAR(50),
	telefono VARCHAR(25),
	sueldo INT,

	PRIMARY KEY(nro_documento, tipo_documento)
};

CREATE TABLE IF NOT EXISTS PersonalLimpieza{
	nro_documento VARCHAR(40),
	tipo_documento VARCHAR(20),

	PRIMARY KEY(nro_documento, tipo_documento),
	CONSTRAINT fk_nro_tipo_documento FOREIGN KEY(nro_documento, tipo_documento) REFERENCES Empleado(nro_documento, tipo_documento)
};

CREATE TABLE IF NOT EXISTS LimpiezaServicio{
	nro_documento VARCHAR(40),
	tipo_documento VARCHAR(20),
	id_servicio INT,

	PRIMARY KEY(nro_documento, tipo_documento),
	PRIMARY KEY(id_servicio),
	CONSTRAINT fk_nro_tipo_documento FOREIGN KEY(nro_documento, tipo_documento) REFERENCES PersonalLimpieza(nro_documento, tipo_documento),
	CONSTRAINT fk_id_servicio FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio)
};
