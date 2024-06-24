CREATE FUNCTION modificar_valor_lodge_tinaja(n_temporada VARCHAR(20), nuevo_valor_lodge INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE Parametro
	SET valor_lodge_tinaja = nuevo_valor_lodge
	WHERE temporada = n_temporada;
	
END
$$ LANGUAGE plpgsql;