#!/bin/sh

http GET "localhost:5000/sueldo?nro_doc=94706789&tipo_doc=chilena"

http GET "localhost:5000/sueldo?nro_doc=A7940349&tipo_doc=mercosur"

http GET "localhost:5000/sueldo?nro_doc=97064907&tipo_doc=pasaporte"
