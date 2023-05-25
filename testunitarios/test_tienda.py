import unittest
import tienda

class TestComprarBillete(unittest.TestCase):
    def setUp(self):
        tienda.app.testing = True
        self.app = tienda.app.test_client()
        
    def test_comprar_billete_exitoso(self):
        data = {
            'nombre': 'pepe',
            'token': 'qPU22DNZ6d'
        }
        response = self.app.post('/comprar', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mensaje'], 'Compra exitosa.')
        
    def test_usuario_no_registrado(self):
        data = {
            'nombre': 'No registrado',
            'token': '1234' 
        }
        response = self.app.post('/comprar', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Usuario no registrado o token incorrecto.')
        
    def test_saldo_insuficiente(self):
        data = {
            'nombre': 'fem',
            'token': 'hwa4u2E0T9'
        }
        response = self.app.post('/comprar', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Saldo insuficiente para comprar el billete.')

if __name__ == '__main__':
    unittest.main()
