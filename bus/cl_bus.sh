#!/bin/bash

BASE_URL="http://localhost:7000"  # URL base del servidor

# Función para realizar una solicitud GET al servidor
function make_get_request() {
    local endpoint="$1"
    curl -s "$BASE_URL$endpoint"
}

# Función para realizar una solicitud PUT al servidor
function make_put_request() {
    local endpoint="$1"
    local payload="$2"
    curl -s -X PUT -H "Content-Type: application/json" -d "$payload" "$BASE_URL$endpoint"
}

# Función para solicitar el número de asiento al usuario
function get_seat_number() {
    read -p "Ingrese el número de asiento: " seat_number
    echo "$seat_number"
}

# Función para solicitar el nombre del cliente al usuario
function get_client_name() {
    read -p "Ingrese el nombre del cliente: " client_name
    echo "$client_name"
}

# Función para mostrar todos los asientos
function show_all_seats() {
    echo "Consultando todos los asientos..."
    response=$(make_get_request "/asientos")
    echo "Asientos: $response"
}

# Función para mostrar los asientos libres
function show_available_seats() {
    echo "Consultando asientos libres..."
    response=$(make_get_request "/asientos/libres")
    echo "Asientos libres: $response"
}

# Función para mostrar los asientos ocupados
function show_occupied_seats() {
    echo "Consultando asientos ocupados..."
    response=$(make_get_request "/asientos/ocupados")
    echo "Asientos ocupados: $response"
}

# Función para ocupar un asiento
function occupy_seat() {
    local seat_number=$(get_seat_number)
    local client_name=$(get_client_name)
    local payload="{\"numero\": $seat_number, \"cliente\": \"$client_name\"}"

    echo "Ocupando el asiento $seat_number..."
    response=$(make_put_request "/asientos/ocupar" "$payload")
    echo "Respuesta: $response"
}

# Función para desocupar un asiento
function release_seat() {
    local seat_number=$(get_seat_number)
    local payload="{\"numero\": $seat_number}"

    echo "Desocupando el asiento $seat_number..."
    response=$(make_put_request "/asientos/desocupar" "$payload")
    echo "Respuesta: $response"
}

# Función principal
function main() {
    while true; do
        echo "=== Aplicación Cliente de Consulta ==="
        echo "1. Mostrar todos los asientos"
        echo "2. Mostrar asientos libres"
        echo "3. Mostrar asientos ocupados"
        echo "4. Ocupar un asiento"
        echo "5. Desocupar un asiento"
        echo "6. Salir"

        read -p "Seleccione una opción: " choice

        case $choice in
        1)
            show_all_seats
            ;;
        2)
            show_available_seats
            ;;
        3)
            show_occupied_seats
            ;;
        4)
            occupy_seat
            ;;
        5)
            release_seat
            ;;
        6)
            echo "¡Hasta luego!"
            break
            ;;
        *)
            echo "Opción inválida. Intente nuevamente."
            ;;
        esac

        echo ""
    done
}

# Ejecutar la función principal
main
