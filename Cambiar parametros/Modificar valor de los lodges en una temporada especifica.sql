CREATE FUNCTION modificar_valor_lodge(n_temporada VARCHAR(20), nuevo_valor_lodge INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE Parametro
	SET valor_lodge = nuevo_valor_lodge
	WHERE temporada = n_temporada;
	
END
$$ LANGUAGE plpgsql;