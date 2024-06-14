CREATE OR REPLACE FUNCTION verificar_reserva()
RETURNS TRIGGER AS $$
BEGIN

	IF (
		SELECT COUNT(*)
		FROM reserva
		WHERE (NEW.fecha_inicio >= reserva.fecha_inicio) AND 
		(NEW.fecha_fin <= reserva.fecha_fin) AND (NEW.id_servicio = reserva.id_servicio) 
	) != 0
	THEN
		RAISE EXCEPTION 'Ya hay una reserva entre esas fechas';
	END IF;

	RETURN NEW;
END
$$ 
LANGUAGE plpgsql;

CREATE TRIGGER verificar_reserva
BEFORE INSERT OR UPDATE ON reserva
FOR EACH ROW
EXECUTE PROCEDURE verificar_reserva();

