#!/bin/sh

http -f GET "localhost:5000/limpieza?nro_doc=94706789&tipo_doc=chilena"

http -f GET "localhost:5000/limpieza?nro_doc=97064907&tipo_doc=pasaporte"
