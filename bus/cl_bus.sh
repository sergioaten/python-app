#!/bin/bash

BASE_URL="http://localhost:7000"

# Obtener el estado de los asientos
get_estado_asientos() {
  curl -s "$BASE_URL/asientos"
}

# Ocupar un asiento
ocupar_asiento() {
  local numero=$1
  local cliente=$2

  curl -s -X PUT -H "Content-Type: application/json" -d '{"numero": '"$numero"', "cliente": "'"$cliente"'"}' "$BASE_URL/asientos/ocupar"
}

# Desocupar un asiento
desocupar_asiento() {
  local numero=$1

  curl -s -X PUT -H "Content-Type: application/json" -d '{"numero": '"$numero"'}' "$BASE_URL/asientos/desocupar"
}

# Mostrar ayuda
mostrar_ayuda() {
  echo "Uso: $0 <acción> [parámetros]"
  echo
  echo "Acciones disponibles:"
  echo "  estado                  Obtener el estado de los asientos"
  echo "  ocupar <número> <cliente>  Ocupar un asiento con un cliente"
  echo "  desocupar <número>       Desocupar un asiento"
}

# Comprobar los argumentos proporcionados
if [ $# -eq 0 ]; then
  mostrar_ayuda
  exit 1
fi

# Realizar la acción correspondiente según los argumentos
accion=$1

case "$accion" in
  "estado")
    get_estado_asientos
    ;;
  "ocupar")
    if [ $# -ne 3 ]; then
      mostrar_ayuda
      exit 1
    fi
    numero=$2
    cliente=$3
    ocupar_asiento "$numero" "$cliente"
    ;;
  "desocupar")
    if [ $# -ne 2 ]; then
      mostrar_ayuda
      exit 1
    fi
    numero=$2
    desocupar_asiento "$numero"
    ;;
  *)
    mostrar_ayuda
    exit 1
    ;;
esac
