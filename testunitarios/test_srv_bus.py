import unittest
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from srv_bus import app, db, Asiento, EstadoAsientos, OcuparAsiento, DesocuparAsiento

class BusTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        self.crear_asientos_iniciales()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def crear_asientos_iniciales(self):
        with self.app:
            with self.ctx:
                for numero_asiento in range(1, 45):
                    asiento = Asiento(numero_asiento)
                    db.session.add(asiento)
                db.session.commit()

    def test_estado_asientos(self):
        with self.app:
            with self.ctx:
                response = self.app.get('/asientos')
                data = response.get_json()

                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(data), 44)

    def test_ocupar_asiento(self):
        with self.app:
            with self.ctx:
                response = self.app.put('/asientos/ocupar', json={'numero': 1, 'cliente': 'John Doe'})
                data = response.get_json()

                self.assertEqual(response.status_code, 200)
                self.assertEqual(data['message'], 'Asiento ocupado exitosamente')

    def test_ocupar_asiento_ocupado(self):
        with self.app:
            with self.ctx:
                self.app.put('/asientos/ocupar', json={'numero': 2, 'cliente': 'Jane Smith'})
                response = self.app.put('/asientos/ocupar', json={'numero': 2, 'cliente': 'John Doe'})
                data = response.get_json()

                self.assertEqual(response.status_code, 400)
                self.assertEqual(data['message'], 'El asiento ya está ocupado')

    def test_desocupar_asiento_libre(self):
        with self.app:
            with self.ctx:
                response = self.app.put('/asientos/desocupar', json={'numero': 3})
                data = response.get_json()

                self.assertEqual(response.status_code, 400)
                self.assertEqual(data['message'], 'El asiento ya está libre')

    def test_desocupar_asiento(self):
        with self.app:
            with self.ctx:
                self.app.put('/asientos/ocupar', json={'numero': 4, 'cliente': 'John Doe'})
                response = self.app.put('/asientos/desocupar', json={'numero': 4})
                data = response.get_json()

                self.assertEqual(response.status_code, 200)
                self.assertEqual(data['message'], 'Asiento desocupado exitosamente')

if __name__ == '__main__':
    unittest.main()
