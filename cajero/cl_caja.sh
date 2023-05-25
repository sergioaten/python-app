#!/bin/bash

BASE_URL="http://localhost:6901"

function make_post_request() {
    local endpoint="$1"
    local data="$2"
    curl -s -H "Content-Type: application/json" -X POST -d "$data" "$BASE_URL$endpoint"
}

function make_get_request() {
    local endpoint="$1"
    curl -s "$BASE_URL$endpoint"
}

function registro_usuario() {
    read -p "Ingrese el nombre: " nombre
    read -p "Ingrese los apellidos: " apellidos

    local data="{\"nombre\":\"$nombre\",\"apellidos\":\"$apellidos\"}"
    local response=$(make_post_request "/registro" "$data")

    local mensaje=$(echo "$response" | jq -r '.mensaje')
    local saldo=$(echo "$response" | jq -r '.saldo')

    echo "Mensaje: $mensaje"
    echo "Saldo: $saldo"
}

function consultar_saldo() {
    read -p "Ingrese el nombre: " nombre

    local response=$(make_get_request "/saldo?nombre=$nombre")

    local saldo=$(echo "$response" | jq -r '.saldo')
    local mensaje=$(echo "$response" | jq -r '.mensaje')

    if [[ "$mensaje" != "null" ]]; then
        echo "Mensaje: $mensaje"
    else
        echo "Saldo: $saldo"
    fi
}

function agregar_saldo() {
    read -p "Ingrese el nombre: " nombre
    read -p "Ingrese los apellidos: " apellidos
    read -p "Ingrese el monto a ingresar: " ingreso

    local data="{\"nombre\":\"$nombre\",\"apellidos\":\"$apellidos\",\"ingreso\":$ingreso}"
    local response=$(make_post_request "/ingreso" "$data")

    local mensaje=$(echo "$response" | jq -r '.mensaje')
    local saldo=$(echo "$response" | jq -r '.saldo')

    echo "Mensaje: $mensaje"
    echo "Saldo: $saldo"
}

function mostrar_menu() {
    echo "========== MENÚ =========="
    echo "1. Registro de usuario"
    echo "2. Consultar saldo"
    echo "3. Agregar saldo"
    echo "9. Salir"
    echo "=========================="
}

while true; do
    mostrar_menu
    read -p "Ingrese una opción: " opcion
    echo

    case $opcion in
        1) registro_usuario ;;
        2) consultar_saldo ;;
        3) agregar_saldo ;;
        9) break ;;
        *) echo "Opción inválida. Por favor, seleccione una opción válida." ;;
    esac

    echo
done

echo "¡Hasta luego!"
