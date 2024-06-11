CREATE TABLE IF NOT EXISTS parametros(
  temporada VARCHAR(20) PRIMARY KEY,
  valor_lodge INTEGER,
  valor_lodge_tinaja INTEGER,
  valor_cabaña INTEGER,
  valor_tinaja INTEGER,
  valro_quincho INTEGER
);

CREATE TABLE IF NOT EXISTS contacto(
  id_contacto SERIAL PRIMARY KEY,
  nombre TEXT,
  telefono VARCHAR(25),
  descripcion TEXT
);

CREATE TABLE IF NOT EXISTS personal_administrativo(
  nro_documento VARCHAR(40),
  tipo_documento VARCHAR(20),

  FOREIGN KEY (nro_documento, tipo_documento) REFERENCES empleado(nro_documento, tipo_documento)
);

CREATE TABLE IF NOT EXISTS administrativo_contacto(
  id_contacto INTEGER,
  nro_doc_empleado VARCHAR(40),
  tipo_doc_empleado VARCHAR(20),

  PRIMARY KEY (id_contacto, nro_doc_empleado, tipo_doc_empleado),

  FOREIGN KEY(id_contacto) REFERENCES contacto(id_contacto),
  FOREIGN KEY(nro_doc_empleado, tipo_doc_empleado) REFERENCES personal_administrativo(nro_documento, tipo_documento),

  CONSTRAINT tipo_de_documento_valido CHECK (tipo_documento IN ('Cédula Chilena', 'Documento Mercosur', 'Pasaporte'))
);
