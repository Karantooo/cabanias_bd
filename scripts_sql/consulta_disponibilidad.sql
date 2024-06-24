CREATE OR REPLACE FUNCTION ObtenerSecuencia(inicio DATE, fin DATE, servicio_nombre VARCHAR(1000))
RETURNS TABLE (servicio VARCHAR(100) , folio_RET INT) AS $$
BEGIN
    RETURN QUERY 
	SELECT servicio.nombre, folio 
	FROM reserva
	INNER JOIN servicio on reserva.id_servicio = servicio.id_servicio
	WHERE (inicio >= fecha_inicio) AND (fin <= fecha_fin) AND (servicio.nombre = servicio_nombre);
END;
$$ LANGUAGE plpgsql;


SELECT * FROM reserva;
SELECT * FROM servicio;


SELECT * FROM ObtenerSecuencia('2024-07-01', '2024-07-02', 'Quincho Grande');