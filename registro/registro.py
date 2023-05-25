import random
import string
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, nombre, apellidos, token):
        self.nombre = nombre
        self.apellidos = apellidos
        self.token = token


with app.app_context():
    db.create_all()


@app.route('/registro', methods=['POST'])
def registro_usuario():
    nombre = request.json.get('nombre')
    apellidos = request.json.get('apellidos')

    if not nombre or not apellidos:
        return jsonify({'error': 'Nombre y apellidos son requeridos'}), 400

    # Generar el token único para la cuenta
    token = generar_token()

    # Crear una nueva instancia del modelo User
    user = User(nombre=nombre, apellidos=apellidos, token=token)

    # Agregar el usuario a la base de datos
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    return jsonify({'token': token}), 201


@app.route('/verificar', methods=['POST'])
def verificar_cuenta():
    nombre = request.json.get('nombre')
    token = request.json.get('token')

    if not nombre or not token:
        return jsonify({'error': 'Nombre y token son requeridos'}), 400

    # Verificar si existe una cuenta con el nombre y el token proporcionados
    with app.app_context():
        user = User.query.filter_by(nombre=nombre, token=token).first()

    if user:
        return jsonify({'existe': True}), 200
    else:
        return jsonify({'existe': False}), 200


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    with app.app_context():
        usuarios = User.query.all()
        resultados = []
        for usuario in usuarios:
            resultados.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellidos': usuario.apellidos,
                'token': usuario.token
            })
        return jsonify(resultados), 200


@app.route('/tokens', methods=['GET'])
def obtener_tokens():
    with app.app_context():
        tokens = [usuario.token for usuario in User.query.all()]
        return jsonify(tokens), 200


@app.route('/basedatos', methods=['GET'])
def obtener_basedatos():
    with app.app_context():
        usuarios = User.query.all()
        resultados = []
        for usuario in usuarios:
            resultados.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellidos': usuario.apellidos,
                'token': usuario.token
            })
        return jsonify({'usuarios': resultados}), 200


def generar_token():
    # Generar un token aleatorio de letras y números con 10 caracteres
    caracteres = string.ascii_letters + string.digits
    token = ''.join(random.choices(caracteres, k=10))
    return token


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6900)
