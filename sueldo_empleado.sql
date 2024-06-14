CREATE OR REPLACE FUNCTION SueldoEmpleado(nro_documento VARCHAR(40))
RETURNS TABLE (sueldo INT) AS $$
BEGIN
    RETURN QUERY 
    SELECT sueldo FROM empleado;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION sueldoempleado;
SELECT * FROM SueldoEmpleado('12345678');