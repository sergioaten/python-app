import unittest
import requests
from  caja import app, db, Usuario


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registro(self):
        with app.app_context():
            response = self.app.post('/registro', json={"nombre": "John", "apellidos": "Doe"})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Usuario registrado con éxito.')
            self.assertEqual(data['saldo'], 100)

    def test_registro_usuario_existente(self):
        with app.app_context():
            usuario = Usuario(nombre="John", apellidos="Doe")
            db.session.add(usuario)
            db.session.commit()

            response = self.app.post('/registro', json={"nombre": "John", "apellidos": "Doe"})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'El usuario ya está registrado.')

    def test_consultar_saldo(self):
        with app.app_context():
            usuario = Usuario(nombre="John", apellidos="Doe", saldo=200)
            db.session.add(usuario)
            db.session.commit()

            response = self.app.get('/saldo?nombre=John')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['saldo'], 200)

    def test_consultar_saldo_usuario_no_encontrado(self):
        with app.app_context():
            response = self.app.get('/saldo?nombre=John')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Usuario no encontrado.')

    def test_realizar_pago_saldo_suficiente(self):
        with app.app_context():
            usuario = Usuario(nombre="John", apellidos="Doe", saldo=200)
            db.session.add(usuario)
            db.session.commit()

            response = self.app.post('/pagar', json={"nombre": "John", "costo": 150})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Pago realizado con éxito.')
            self.assertEqual(data['saldo'], 50)

    def test_realizar_pago_saldo_insuficiente(self):
        with app.app_context():
            usuario = Usuario(nombre="John", apellidos="Doe", saldo=50)
            db.session.add(usuario)
            db.session.commit()

            response = self.app.post('/pagar', json={"nombre": "John", "costo": 100})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Saldo insuficiente.')

    def test_realizar_pago_usuario_no_encontrado(self):
        with app.app_context():
            response = self.app.post('/pagar', json={"nombre": "John", "costo": 100})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Usuario no encontrado.')

    def test_agregar_saldo(self):
        with app.app_context():
            usuario = Usuario(nombre="John", apellidos="Doe", saldo=100)
            db.session.add(usuario)
            db.session.commit()

            response = self.app.post('/ingreso', json={"nombre": "John", "apellidos": "Doe", "ingreso": 50})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Ingreso realizado con éxito.')
            self.assertEqual(data['saldo'], 150)

    def test_agregar_saldo_usuario_no_encontrado(self):
        with app.app_context():
            response = self.app.post('/ingreso', json={"nombre": "John", "apellidos": "Doe", "ingreso": 50})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['mensaje'], 'Usuario no encontrado.')


if __name__ == '__main__':
    unittest.main()
