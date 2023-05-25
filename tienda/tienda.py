import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
REGISTRO_API_URL = 'http://localhost:6900/verificar'
PLAZAS_API_URL = 'http://localhost:7000/asientos'
PAGAR_API_URL = 'http://localhost:6901/pagar'


@app.route('/comprar', methods=['POST'])
def comprar_billete():
    data = request.get_json()
    nombre = data.get('nombre')
    token = data.get('token')
    valor_billete = 150

    # Verificar si el usuario está registrado y el token es correcto
    response_registro = requests.post(REGISTRO_API_URL, json={'nombre': nombre, 'token': token})
    if response_registro.status_code != 200 or not response_registro.json().get('existe'):
        return jsonify({'mensaje': 'Usuario no registrado o token incorrecto.'}), 400

    # Verificar si existen plazas libres
    response_plazas = requests.get(PLAZAS_API_URL)
    plazas_estado = response_plazas.json()
    #print(plazas_estado)
    plazas_libres = [numero for numero, estado in plazas_estado.items() if estado['estado'] == 'libre']
    if not plazas_libres:
        return jsonify({'mensaje': 'No hay plazas libres disponibles.'}), 400

    # Verificar si el usuario tiene saldo suficiente
    response_saldo = requests.get(f'http://localhost:6901/saldo?nombre={nombre}')
    if response_saldo.status_code != 200 or response_saldo.json().get('saldo', 0) < valor_billete:
        return jsonify({'mensaje': 'Saldo insuficiente para comprar el billete.'}), 400

    # Realizar el pago
    response_pago = requests.post(PAGAR_API_URL, json={'nombre': nombre, 'costo': valor_billete})
    if response_pago.status_code != 200 or not response_pago.json().get('mensaje') == 'Pago realizado con éxito.':
        return jsonify({'mensaje': 'Error al procesar el pago.'}), 500

    # Ocupar un asiento
    asiento_a_ocupar = plazas_libres[0]
    response_ocupar = requests.put(f'http://localhost:7000/asientos/ocupar', json={'numero': asiento_a_ocupar, 'cliente': nombre})
    if response_ocupar.status_code != 200 or not response_ocupar.json().get('message') == 'Asiento ocupado exitosamente':
        return jsonify({'mensaje': 'Error al ocupar el asiento.'}), 500

    return jsonify({
        'mensaje': 'Compra exitosa.',
        'asiento': asiento_a_ocupar,
        'saldo': response_saldo.json().get('saldo')
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
