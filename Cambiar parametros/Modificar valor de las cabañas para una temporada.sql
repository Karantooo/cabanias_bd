CREATE FUNCTION modificar_valor_cabana(n_temporada VARCHAR(20), nuevo_valor_cabana INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE Parametro
	SET valor_cabana = nuevo_valor_cabana
	WHERE temporada = n_temporada;
	
END
$$ LANGUAGE plpgsql;