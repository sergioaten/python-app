import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import registro

class RegistroTestCase(unittest.TestCase):
    def setUp(self):
        registro.app.testing = True
        self.app = registro.app.test_client()
        self.ctx = registro.app.app_context()
        self.ctx.push()
        registro.db.create_all()

    def tearDown(self):
        registro.db.session.remove()
        registro.db.drop_all()
        self.ctx.pop()

    def test_registro_usuario(self):
        payload = {
            'nombre': 'John',
            'apellidos': 'Doe'
        }
        response = self.app.post('/registro', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('token', data)

    def test_registro_usuario_sin_nombre(self):
        payload = {
            'apellidos': 'Doe'
        }
        response = self.app.post('/registro', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_verificar_cuenta(self):
        payload = {
            'nombre': 'John',
            'token': 'randomtoken'
        }
        response = self.app.post('/verificar', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('existe', data)
        self.assertEqual(data['existe'], False)

if __name__ == '__main__':
    unittest.main()
