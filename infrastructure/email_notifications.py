
from typing import Dict
import requests
from settings import log, SETTINGS

class EmailService:
    def __init__(self) -> None:
        self._http_service = requests
        self._base_url_api = 'https://api.brevo.com/v3/smtp/email'
        self._headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'api-key': SETTINGS.api_key_brevo
        }

    def send_email_with_template(
        self, 
        email_receiver: str,
        template_id: int,
        template_data: Dict[str, any]
    )->int:
        try:
            response = self._http_service.post(
                url=self._base_url_api,
                headers=self._headers,
                json={  
                    "to":[  
                        {  
                            "email":email_receiver
                        }
                    ],
                    "templateId": template_id,
                    "params": template_data
                }
            )
            log.info(response)

        except Exception as e:
            log.error(f'Error en el envio de corre {e}')

        return True
