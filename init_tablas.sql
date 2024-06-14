CREATE TABLE Cliente(
    nro_documento VARCHAR(40),
    tipo_documento VARCHAR(20),
    nombre VARCHAR(100),
    nacionalidad VARCHAR(100),
    correo VARCHAR(50),
    telefono VARCHAR(25),
    
    PRIMARY KEY (nro_documento, tipo_documento),
    CONSTRAINT tipo_de_documento_valido CHECK (tipo_documento IN ('Cédula Chilena', 'Documento Mercosur', 'Pasaporte'))
    
);

CREATE TABLE Factura(
    folio INT PRIMARY KEY,
    valor INT CHECK (valor >= 0),
    fecha DATE,
    estado VARCHAR(10),

    CONSTRAINT estado_pago CHECK(estado IN ('PAGADO', 'NO PAGADO'))
);
CREATE TABLE Servicio( id_servicio INT PRIMARY KEY,
    nombre VARCHAR(100),
    capacidad INT,
    tipo_servicio VARCHAR(30),

    CONSTRAINT servicios_disponibles CHECK(tipo_servicio IN ('QUINCHO', 'TINAJA', 'HOSPEDAJE'))
);


CREATE TABLE Reserva(
    id_reserva INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cant_personas INT CHECK (cant_personas >= 1),
    nro_documento_cliente VARCHAR(40),
    tipo_documento_cliente VARCHAR(20),
    id_servicio INT,
    folio INT,
    fecha_inicio DATE,
    fecha_fin DATE,


    FOREIGN KEY (nro_documento_cliente, tipo_documento_cliente) REFERENCES Cliente(nro_documento, tipo_documento), 
    FOREIGN KEY (folio) REFERENCES Factura(folio),
    FOREIGN KEY (id_servicio) REFERENCES Servicio(id_servicio) 
);


CREATE TABLE IF NOT EXISTS Hospedaje(
    id_servicio INT PRIMARY KEY,
    cant_camas_dobles INT,
    cant_camas_single INT,
    
    FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio)
);

CREATE TABLE IF NOT EXISTS Cabana(
    id_servicio INT PRIMARY KEY,
    cant_habitaciones INT,
    
    FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio)
);

CREATE TABLE IF NOT EXISTS Lodge(
    id_servicio INT PRIMARY KEY,
    con_tinaja CHAR(3),

    FOREIGN KEY(id_servicio) REFERENCES Servicio(id_servicio),

    CONSTRAINT opcion_con_tinaja_valida CHECK (con_tinaja IN ('SIN','CON'))
);

CREATE TABLE IF NOT EXISTS Empleado(
    nro_documento VARCHAR(40),
    tipo_documento VARCHAR(20),
    nombre VARCHAR(100),
    correo VARCHAR(50),
    telefono VARCHAR(25),
    sueldo INT,

    PRIMARY KEY(nro_documento, tipo_documento)
    CONSTRAINT tipo_de_documento_valido CHECK (tipo_documento IN ('Cédula Chilena', 'Documento Mercosur', 'Pasaporte'))
);

CREATE TABLE IF NOT EXISTS PersonalLimpieza(
    nro_documento VARCHAR(40),
    tipo_documento VARCHAR(20),

    PRIMARY KEY(nro_documento, tipo_documento),

    FOREIGN KEY(nro_documento, tipo_documento) REFERENCES Empleado(nro_documento, tipo_documento)
);

CREATE TABLE IF NOT EXISTS LimpiezaServicio(
    nro_documento VARCHAR(40),
    tipo_documento VARCHAR(20),
    id_servicio INT,

    PRIMARY KEY (nro_documento, tipo_documento, id_servicio),

    FOREIGN KEY (nro_documento, tipo_documento) REFERENCES PersonalLimpieza(nro_documento, tipo_documento),
    FOREIGN KEY (id_servicio) REFERENCES Servicio(id_servicio)
);

CREATE TABLE IF NOT EXISTS Parametros(
     temporada VARCHAR(20) PRIMARY KEY,
     valor_lodge INTEGER CHECK (valor_lodge > 0),
     valor_lodge_tinaja INTEGER CHECK (valor_lodge_tinaja > 0),
     valor_cabana INTEGER CHECK (valor_cabana > 0),
     valor_tinaja INTEGER CHECK (valor_tinaja > 0),
     valor_quincho INTEGER CHECK (valor_quincho > 0)
);

CREATE TABLE IF NOT EXISTS Contacto(
     id_contacto SERIAL PRIMARY KEY,
     nombre TEXT,
     telefono VARCHAR(25),
     descripcion TEXT
);

CREATE TABLE IF NOT EXISTS PersonalAdministrativo(
     nro_documento VARCHAR(40),
     tipo_documento VARCHAR(20),
     PRIMARY KEY (nro_documento, tipo_documento), 
    
     FOREIGN KEY (nro_documento, tipo_documento) REFERENCES Empleado(nro_documento, tipo_documento)
);

CREATE TABLE IF NOT EXISTS AdministrativoContacto(
     id_contacto INTEGER,
     nro_doc_empleado VARCHAR(40),
     tipo_doc_empleado VARCHAR(20),

     PRIMARY KEY (id_contacto, nro_doc_empleado, tipo_doc_empleado),

     FOREIGN KEY (id_contacto) REFERENCES Contacto(id_contacto),
     FOREIGN KEY (nro_doc_empleado, tipo_doc_empleado) REFERENCES PersonalAdministrativo(nro_documento, tipo_documento),
);
