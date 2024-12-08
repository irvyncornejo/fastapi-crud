import logging
from pydantic_settings import BaseSettings
from functools import lru_cache

log = logging.getLogger('uvicorn.error')

class ApiSettings(BaseSettings):
    auth_secrets_key: str = ''
    mongo_conn_str: str = ''
    env:str = ''
    api_key_brevo:str = ''
    api_service_url:str = ''
    secret_key:str = ''
    users_db_name:str = ''
    users_colecction_name:str=''
    admin_email:str=''
    admin_password:str=''

    class Config:
        env_file = '.env'

@lru_cache()
def get_settings() -> ApiSettings:
    return ApiSettings()

SETTINGS = get_settings()
