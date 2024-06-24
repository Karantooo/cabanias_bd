#!/bin/sh

http GET "localhost:5000/cliente?nro_doc=12345678&tipo_doc=chilena"

http GET "localhost:5000/cliente?nro_doc=33445566&tipo_doc=chilena"

http GET "localhost:5000/cliente?nro_doc=B7654321&tipo_doc=pasaporte"
