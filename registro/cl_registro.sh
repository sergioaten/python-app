#!/bin/bash

BASE_URL="http://localhost:6900"

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
    make_post_request "/registro" "$data"
}

function verificar_cuenta() {
    read -p "Ingrese el nombre: " nombre
    read -p "Ingrese el token: " token

    local data="{\"nombre\":\"$nombre\",\"token\":\"$token\"}"
    make_post_request "/verificar" "$data"
}

function obtener_usuarios() {
    make_get_request "/usuarios"
}

function obtener_tokens() {
    make_get_request "/tokens"
}

function obtener_basedatos() {
    make_get_request "/basedatos"
}

function mostrar_menu() {
    echo "========== MENÚ =========="
    echo "1. Registrar usuario"
    echo "2. Verificar cuenta"
    echo "3. Obtener usuarios"
    echo "4. Obtener tokens"
    echo "5. Obtener base de datos"
    echo "0. Salir"
    echo "=========================="
}

while true; do
    mostrar_menu
    read -p "Ingrese una opción: " opcion
    echo

    case $opcion in
        1) registro_usuario ;;
        2) verificar_cuenta ;;
        3) obtener_usuarios ;;
        4) obtener_tokens ;;
        5) obtener_basedatos ;;
        0) break ;;
        *) echo "Opción inválida. Por favor, seleccione una opción válida." ;;
    esac

    echo
done

echo "¡Hasta luego!"
