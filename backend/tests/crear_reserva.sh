#!/bin/sh

http -f POST localhost:5000/reserva cant_personas=4 \
  nro_doc=12345678 tipo_doc='chilena' servicio=102 \
  fecha_inicio='2024-06-15' fecha_fin='2024-06-18'

http -f POST localhost:5000/reserva cant_personas=4 \
  nro_doc=A1234567 tipo_doc='pasaporte' servicio=205 \
  fecha_inicio='2024-06-21' fecha_fin='2024-06-25'

http -f POST localhost:5000/reserva cant_personas=4 \
  nro_doc=66778899 tipo_doc='mercosur' servicio=101 \
  fecha_inicio='2024-07-10' fecha_fin='2024-07-15'

http -f POST localhost:5000/reserva cant_personas=4 \
  nro_doc=66778899 tipo_doc='mercosur' servicio=800 \
  folio=6 fecha_inicio='2024-07-12' fecha_fin='2024-07-12'
