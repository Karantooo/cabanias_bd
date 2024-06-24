CREATE OR REPLACE FUNCTION SueldoEmpleado(nro_documento_func VARCHAR(40), tipo_documento_func VARCHAR(20))
RETURNS TABLE (sueldo INT) AS $$
BEGIN
    RETURN QUERY 
    SELECT empleado.sueldo FROM empleado
	WHERE (empleado.nro_documento = nro_documento_func) AND (empleado.tipo_documento = tipo_documento_func);
END;
$$ LANGUAGE plpgsql;


SELECT * FROM SueldoEmpleado('12345678', 'Pasaporte');