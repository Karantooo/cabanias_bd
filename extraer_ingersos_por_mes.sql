CREATE OR REPLACE FUNCTION SumarValoresPorMes(mes DATE)
RETURNS NUMERIC AS $$
DECLARE
    suma NUMERIC;
BEGIN
    SELECT SUM(valor) INTO suma
    FROM factura
    WHERE EXTRACT(YEAR FROM mes) = EXTRACT(YEAR FROM factura.fecha)
    AND EXTRACT(MONTH FROM mes) = EXTRACT(MONTH FROM factura.fecha);
    
    RETURN suma;
END; $$
LANGUAGE plpgsql;

SELECT *
FROM SumarValoresPorMes('2024-03-05');




