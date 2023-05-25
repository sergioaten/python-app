#!/bin/bash

read -p "Nombre: " nombre
read -p "Apellidos: " apellidos
read -p "Token: " token

curl -X POST -H "Content-Type: application/json" -d "{\"nombre\": \"$nombre\", \"apellidos\": \"$apellidos\", \"token\": \"$token\"}" http://localhost:8888/comprar
