CREATE FUNCTION crear_cliente(new_nro_documento VARCHAR(40), new_tipo_documento VARCHAR(20), new_nombre VARCHAR(100), new_nacionalidad VARCHAR(100), new_correo VARCHAR(50), new_telefono VARCHAR(25))
RETURNS VOID AS $$
BEGIN
    INSERT INTO Cliente(nro_documento, tipo_documento, nombre, nacionalidad, correo, telefono)
    VALUES(new_nro_documento, new_tipo_documento, new_nombre, new_nacionalidad, new_correo, new_telefono);
END
$$ LANGUAGE plpgsql;