#!/bin/sh

http -f POST localhost:5000/cliente nro_doc=11111111-6 \
  tipo_doc="chilena" nombre=Pedro \
  nacionalidad=CL correo=contacto@example.org telefono=45679789456

http -f POST localhost:5000/cliente nro_doc=A45697254 \
  tipo_doc="pasaporte" nombre=Vladimir \
  nacionalidad=RU correo=contacto@example.org telefono=45679789456

http -f POST localhost:5000/cliente nro_doc=4569756 \
  tipo_doc="mercosur" nombre=Ricardo \
  nacionalidad=US correo=contacto@example.org telefono=45679789456
