CREATE OR REPLACE FUNCTION ServicioLimpiezaEmpleado(nro_empleado VARCHAR(40), tipo_documento_empleado VARCHAR(20))
RETURNS TABLE (nombre VARCHAR(50), nro_empleado_RET VARCHAR(40)) AS $$
BEGIN
    RETURN QUERY 
	SELECT servicio.nombre, empleado.nro_documento
	FROM limpiezaservicio
	INNER JOIN empleado 
	ON (empleado.nro_documento = limpiezaservicio.nro_documento) AND (empleado.tipo_documento = limpiezaservicio.tipo_documento)
	INNER JOIN servicio
	ON servicio.id_servicio = limpiezaservicio.id_servicio
	WHERE (empleado.nro_documento = nro_empleado) AND (empleado.tipo_documento = tipo_documento_empleado);
		
END;
$$ LANGUAGE plpgsql;


SELECT * FROM ServicioLimpiezaEmpleado('12345678', 'Pasaporte');




