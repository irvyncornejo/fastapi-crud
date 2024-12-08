import unittest

from parameterized import parameterized
from faker import Faker

from .config_client import get_token, client

faker = Faker()
ADMIN_TEST = {"username": "admin@bp.com", "password": "56er%hji90G"}

class TestUsersApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUsersApi, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.admin_token = get_token(**ADMIN_TEST).json()

    @parameterized.expand([
        [ADMIN_TEST, 200],
        [{"username": faker.email(), "password": "invalid_password"}, 401],
        [{"username": faker.name(), "password": "skjhsdhsjk"}, 401]
    ])


    def test_get_token(self, data, status_code):
        response = get_token(**data)
        assert(response.status_code == status_code)
    

    @parameterized.expand([
        [{  
            "email": faker.email(),
            "full_name": faker.name(),
            "password": faker.password(),
            "role": "films"
        }, 201],
    ])

    def test_create_user(self, data, status_code):
        print(data)
        response = client.post(
            'api/users',
            json=data,
            headers={'Bearer': self.admin_token['access_token']}
        )
        print(response)
        assert(response.status_code == 201)
    
    @classmethod
    def tearDownClass(cls):
        print('Cerrando')
