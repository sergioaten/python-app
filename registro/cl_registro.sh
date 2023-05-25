#!/bin/bash
# Función para mostrar el uso del script
mostrar_uso() {
    echo "Uso: $0 [opciones]"
    echo "Opciones:"
    echo "  -a, --agregar     Agregar una cuenta de usuario"
    echo "  -c, --consultar   Consultar la existencia de una cuenta de usuario"
    exit 1
}

# Función para agregar una cuenta de usuario
agregar_cuenta() {
    nombre=$1
    apellido=$2
    registro_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"nombre": "'$nombre'", "apellidos": "'$apellido'"}' http://localhost:6900/registro)
    token=$(echo $registro_response | jq -r '.token')
    echo "Token de la cuenta registrada: $token"
}

# Función para consultar la existencia de una cuenta de usuario
consultar_cuenta() {
    nombre=$1
    token=$2
    verificar_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"nombre": "'$nombre'", "token": "'$token'"}' http://localhost:6900/verificar)
    existe=$(echo $verificar_response | jq -r '.existe')

    if [[ $existe == "true" ]]; then
        echo "La cuenta con el token $token existe"
    else
        echo "La cuenta con el token $token no existe"
    fi
}

# Parsear los argumentos de línea de comandos
case $1 in
     -a|--agregar)
		agregar_cuenta $2 $3
      ;;
     -c|--consultar)
		consultar_cuenta $2 $3
     ;;
     *)
       mostrar_uso
    ;;
esac
