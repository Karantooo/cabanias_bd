CREATE OR REPLACE FUNCTION ObtenerSecuencia(inicio DATE, fin DATE, servicio_nombre VARCHAR(1000))
RETURNS TABLE (servicio VARCHAR(100) , folio INT) AS $$
BEGIN
    RETURN QUERY 
	SELECT servicio.nombre, folio 
	FROM reserva
	INNER JOIN servicio on reserva.id_servicio = servicio.id_servicio
	WHERE (fecha_inicio = inicio) AND (fecha_fin = fin) AND (servicio.nombre = servicio_nombre);
END;
$$ LANGUAGE plpgsql;


