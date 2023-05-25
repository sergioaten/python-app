from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus.db'  # Configura la URL de la base de datos
db = SQLAlchemy(app)

# Definición del modelo de la tabla de asientos
class Asiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True)
    estado = db.Column(db.String(10))
    ocupante = db.Column(db.String(50))

    def __init__(self, numero):
        self.numero = numero
        self.estado = 'libre'
        self.ocupante = ''

# Crear los asientos iniciales
def crear_asientos_iniciales():
    for numero_asiento in range(1, 45):
        # Verificar si el asiento ya existe
        if Asiento.query.filter_by(numero=numero_asiento).first() is None:
            asiento = Asiento(numero_asiento)
            db.session.add(asiento)
    db.session.commit()

# Definición del recurso para obtener el estado de los asientos
class EstadoAsientos(Resource):
    def get(self):
        asientos = Asiento.query.all()
        estado = {asiento.numero: {'estado': asiento.estado, 'ocupante': asiento.ocupante} for asiento in asientos}
        return jsonify(estado)

# Definición del recurso para ocupar un asiento
class OcuparAsiento(Resource):
    def put(self):
        numero = request.json.get('numero')
        cliente = request.json.get('cliente')
        
        if not numero or not cliente:
            return {'message': 'Número de asiento y cliente son requeridos'}, 400
        
        asiento = Asiento.query.filter_by(numero=numero).first()
        
        if not asiento:
            return {'message': 'Asiento no encontrado'}, 404
        
        if asiento.estado == 'ocupado':
            return {'message': 'El asiento ya está ocupado'}, 400
        
        asiento.estado = 'ocupado'
        asiento.ocupante = cliente
        
        db.session.commit()
        
        return {'message': 'Asiento ocupado exitosamente'}, 200

# Definición del recurso para desocupar un asiento
class DesocuparAsiento(Resource):
    def put(self):
        numero = request.json.get('numero')
        
        if not numero:
            return {'message': 'Número de asiento es requerido'}, 400
        
        asiento = Asiento.query.filter_by(numero=numero).first()
        
        if not asiento:
            return {'message': 'Asiento no encontrado'}, 404
        
        if asiento.estado == 'libre':
            return {'message': 'El asiento ya está libre'}, 400
        
        asiento.estado = 'libre'
        asiento.ocupante = ''
        
        db.session.commit()
        
        return {'message': 'Asiento desocupado exitosamente'}, 200

# Definición del recurso para consultar los asientos libres
class AsientosLibres(Resource):
    def get(self):
        asientos_libres = Asiento.query.filter_by(estado='libre').all()
        numeros_libres = [asiento.numero for asiento in asientos_libres]
        return jsonify({'asientos_libres': numeros_libres})

# Definición del recurso para consultar los asientos ocupados
class AsientosOcupados(Resource):
    def get(self):
        asientos_ocupados = Asiento.query.filter_by(estado='ocupado').all()
        numeros_ocupados = [asiento.numero for asiento in asientos_ocupados]
        return jsonify({'asientos_ocupados': numeros_ocupados})

# Agregar los recursos a la API
api.add_resource(EstadoAsientos, '/asientos')
api.add_resource(OcuparAsiento, '/asientos/ocupar')
api.add_resource(DesocuparAsiento, '/asientos/desocupar')
api.add_resource(AsientosLibres, '/asientos/libres')
api.add_resource(AsientosOcupados, '/asientos/ocupados')

if __name__ == '__main__':
    with app.app_context():
        # Crear la base de datos y definir los modelos
        db.create_all()

        # Crear los asientos iniciales
        crear_asientos_iniciales()

    # Iniciar la aplicación Flask
    app.run(host='0.0.0.0', port=7000)
