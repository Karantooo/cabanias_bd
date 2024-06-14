INSERT INTO cliente
VALUES (5, 'Pasaporte', 'Juan Perez', 'Peruana', 'juan_perez@gmail.com', 4862465);

-- Insertar clientes con diferentes tipos de documento y valores variados
INSERT INTO Cliente (nro_documento, tipo_documento, nombre, nacionalidad, correo, telefono)
VALUES 
('12345678', 'Cédula Chilena', 'Ana Gomez', 'Chilena', 'ana_gomez@gmail.com', '12345678'),
('87654321', 'Documento Mercosur', 'Carlos Mendez', 'Argentina', 'carlos_mendez@gmail.com', '87654321'),
('A1234567', 'Pasaporte', 'Beatriz Fernández', 'Peruana', 'beatriz_fernandez@gmail.com', '98765432');

-- Otro conjunto de inserciones
INSERT INTO Cliente (nro_documento, tipo_documento, nombre, nacionalidad, correo, telefono)
VALUES 
('22334455', 'Cédula Chilena', 'Roberto Silva', 'Chilena', 'roberto_silva@gmail.com', '22334455'),
('55667788', 'Documento Mercosur', 'Mariana Lopez', 'Brasilera', 'mariana_lopez@gmail.com', '55667788'),
('B7654321', 'Pasaporte', 'Jorge Martínez', 'Uruguaya', 'jorge_martinez@gmail.com', '11223344');

-- Otro conjunto adicional de inserciones
INSERT INTO Cliente (nro_documento, tipo_documento, nombre, nacionalidad, correo, telefono)
VALUES 
('33445566', 'Cédula Chilena', 'Sofía Rodríguez', 'Chilena', 'sofia_rodriguez@gmail.com', '33445566'),
('66778899', 'Documento Mercosur', 'Lucas Gonzales', 'Paraguaya', 'lucas_gonzales@gmail.com', '66778899'),
('C9876543', 'Pasaporte', 'Valentina Herrera', 'Boliviana', 'valentina_herrera@gmail.com', '99887766');


-- Insertar facturas con diferentes valores, fechas y estados
INSERT INTO Factura (folio, valor, fecha, estado)
VALUES
(1, 100000, '2024-01-15', 'PAGADO'),
(2, 200000, '2024-02-10', 'NO PAGADO'),
(3, 150000, '2024-03-05', 'PAGADO'),
(4, 250000, '2024-04-20', 'NO PAGADO'),
(5, 300000, '2024-05-15', 'PAGADO');

-- Otro conjunto de inserciones
INSERT INTO Factura (folio, valor, fecha, estado)
VALUES
(6, 180000, '2024-06-18', 'NO PAGADO'),
(7, 120000, '2024-07-25', 'PAGADO'),
(8, 220000, '2024-08-12', 'NO PAGADO'),
(9, 160000, '2024-09-09', 'PAGADO'),
(10, 270000, '2024-10-22', 'NO PAGADO');

-- Otro conjunto adicional de inserciones
INSERT INTO Factura (folio, valor, fecha, estado)
VALUES
(11, 210000, '2024-11-15', 'PAGADO'),
(12, 190000, '2024-12-05', 'NO PAGADO'),
(13, 140000, '2024-01-28', 'PAGADO'),
(14, 230000, '2024-02-16', 'NO PAGADO'),
(15, 250000, '2024-03-30', 'PAGADO');
