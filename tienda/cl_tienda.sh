#!/bin/bash

BASE_URL="http://localhost:8888"

function make_post_request() {
    local endpoint="$1"
    local data="$2"
    curl -s -H "Content-Type: application/json" -X POST -d "$data" "$BASE_URL$endpoint"
}

function make_get_request() {
    local endpoint="$1"
    curl -s "$BASE_URL$endpoint"
}

function comprar_billete() {
    read -p "Ingrese el nombre: " nombre
    read -p "Ingrese el token: " token

    local data="{\"nombre\":\"$nombre\",\"token\":\"$token\"}"
    local response=$(make_post_request "/comprar" "$data")

    local mensaje=$(echo "$response" | jq -r '.mensaje')
    local asiento=$(echo "$response" | jq -r '.asiento')
    local saldo=$(echo "$response" | jq -r '.saldo')

    echo "Mensaje: $mensaje"
    echo "Asiento: $asiento"
    echo "Saldo: $saldo"
}

function mostrar_menu() {
    echo "========== MENÚ =========="
    echo "1. Comprar billete"
    echo "9. Salir"
    echo "=========================="
}

while true; do
    mostrar_menu
    read -p "Ingrese una opción: " opcion
    echo

    case $opcion in
        1) comprar_billete ;;
        9) break ;;
        *) echo "Opción inválida. Por favor, seleccione una opción válida." ;;
    esac

    echo
done

echo "¡Hasta luego!"
