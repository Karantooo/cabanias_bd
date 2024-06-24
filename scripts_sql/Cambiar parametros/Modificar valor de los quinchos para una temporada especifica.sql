CREATE FUNCTION modificar_valor_quincho(n_temporada VARCHAR(20), nuevo_valor_quincho INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE Parametro
	SET valor_quincho = nuevo_valor_tinaja
	WHERE temporada = n_temporada;
	
END
$$ LANGUAGE plpgsql;