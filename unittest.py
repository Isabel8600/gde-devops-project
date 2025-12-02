import unittest
import json
from app import app, STATUS_MESSAGE, EXPECTED_STATUS_CODE

class AppTestCase(unittest.TestCase):
    """
    Unit teszt osztály az 'app.py' Flask alkalmazáshoz.
    """

    def setUp(self):
        """
        Előkészíti a tesztkörnyezetet: létrehoz egy tesztklienst.
        """
        # Beállítjuk a Flask alkalmazást tesztelés módra
        app.config['TESTING'] = True
        # Létrehozunk egy tesztklienst, amivel HTTP kéréseket küldhetünk
        self.client = app.test_client()
    
    def test_status_endpoint_success(self):
        """
        Ellenőrzi, hogy a /status végpont sikeres (HTTP 200) választ ad-e vissza,
        és tartalmazza-e a meghatározott üzenetet.
        """
        # GET kérés küldése a /status végpontra
        response = self.client.get('/status')

        # Ellenőrizzük a HTTP státuszkódot
        self.assertEqual(response.status_code, EXPECTED_STATUS_CODE)

        # Ellenőrizzük, hogy a válasz JSON formátumú
        self.assertEqual(response.content_type, 'application/json')
        
        # JSON tartalom dekódolása
        data = json.loads(response.get_data(as_text=True))
        
        # Ellenőrizzük, hogy a válasz tartalmazza-e a feladatban kért stringet
        self.assertIn('message', data)
        self.assertEqual(data['message'], STATUS_MESSAGE)

    def test_home_endpoint_success(self):
        """
        Ellenőrzi, hogy a főoldal (/) végpont is sikeres (HTTP 200) választ ad-e.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, EXPECTED_STATUS_CODE)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('info', data)


if __name__ == '__main__':
    # A tesztek futtatása a Python unittest moduljával
    unittest.main()