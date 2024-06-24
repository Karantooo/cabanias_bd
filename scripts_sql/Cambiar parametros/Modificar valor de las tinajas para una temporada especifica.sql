CREATE FUNCTION modificar_valor_tinaja(n_temporada VARCHAR(20), nuevo_valor_tinaja INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE Parametro
	SET valor_tinaja = nuevo_valor_tinaja
	WHERE temporada = n_temporada;
	
END
$$ LANGUAGE plpgsql;