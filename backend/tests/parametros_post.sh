#!/bin/sh

http -f POST localhost:5000/temporada temporada='Primavera 2024' \
  fecha_inicio='2024-08-15' fecha_fin='2024-11-22' lodge=45000 \
  lodge_tinaja=60000 cabana=75000 tinaja=40000 quincho=60000

http -f POST localhost:5000/temporada temporada='Verano 2025' \
  fecha_inicio='2024-08-15' fecha_fin='2024-11-22' lodge=65000 \
  lodge_tinaja=80000 cabana=140000 tinaja=40000 quincho=60000
