#!/bin/sh

http -f GET "localhost:5000/temporada"

http -f GET "localhost:5000/temporada?fecha=2024-05-10"

