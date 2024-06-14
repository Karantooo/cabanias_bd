CREATE OR REPLACE FUNCTION ObtenerSecuencia(nro_documento VARCHAR(40), tipo_documento VARCHAR(20))
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


SELECT * FROM ObtenerSecuencia('12345678', 'Cédula Chilena');


