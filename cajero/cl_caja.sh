#!/bin/bash

URL="http://localhost:6901"  # Cambia la URL según la dirección del servidor

# Función para mostrar el resultado de la solicitud HTTP
function show_result() {
    echo "Respuesta del servidor:"
    echo "$1"
    echo
}

# Registro de usuario
function registrar_usuario() {
    nombre=$1
    apellidos=$2

    echo "Registro de usuario"
    echo "Nombre: $nombre"
    echo "Apellidos: $apellidos"
    echo

    result=$(curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"nombre\":\"$nombre\",\"apellidos\":\"$apellidos\"}" \
        "$URL/registro")
    show_result "$result"
}

# Ingreso de dinero
function ingresar_dinero() {
    nombre=$1
    apellidos=$2
    ingreso=$3

    echo "Ingresar dinero"
    echo "Nombre: $nombre"
    echo "Apellidos: $apellidos"
    echo "Ingreso: $ingreso"
    echo

    result=$(curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"nombre\":\"$nombre\",\"apellidos\":\"$apellidos\",\"ingreso\":$ingreso}" \
        "$URL/ingreso")
    show_result "$result"
}

# Consulta de saldo
function consultar_saldo() {
    nombre=$1

    echo "Consultar saldo"
    echo "Nombre: $nombre"
    echo

    result=$(curl -s "$URL/saldo?nombre=$nombre")
    show_result "$result"
}

# Realizar compra
function realizar_compra() {
    nombre=$1
    costo=$2

    echo "Realizar compra"
    echo "Nombre: $nombre"
    echo "Costo: $costo"
    echo

    result=$(curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"nombre\":\"$nombre\",\"costo\":$costo}" \
        "$URL/pagar")
    show_result "$result"
}

# Comandos disponibles
echo "Aplicación Cliente"
echo "1. Registrar usuario"
echo "2. Ingresar dinero"
echo "3. Consultar saldo"
echo "4. Realizar compra"
echo

read -p "Ingrese el número de comando: " comando

case $comando in
    1)
        read -p "Nombre: " nombre
        read -p "Apellidos: " apellidos
        registrar_usuario "$nombre" "$apellidos"
        ;;
    2)
        read -p "Nombre: " nombre
        read -p "Apellidos: " apellidos
        read -p "Ingreso: " ingreso
        ingresar_dinero "$nombre" "$apellidos" $ingreso
        ;;
    3)
        read -p "Nombre: " nombre
        consultar_saldo "$nombre"
        ;;
    4)
        read -p "Nombre: " nombre
        read -p "Costo de la compra: " costo
        realizar_compra "$nombre" $costo
        ;;
    *)
        echo "Comando inválido"
        ;;
esac
