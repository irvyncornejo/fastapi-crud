import requests
from settings import log

class ApiProvider:
    def __init__(self):
        self._url = 'https://ghibliapi.vercel.app/'

    def retrieve_data(self, role:str):
        try:
            data = requests.get(f'{self._url}{role}')
            if data.status_code != 200:
                return None
            return data.json()

        except Exception as e:
            log.error(f'Error al solicitar api de ghilbi {e}')
            return None
