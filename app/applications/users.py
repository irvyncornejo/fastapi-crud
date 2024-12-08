from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.security import OAuth2PasswordBearer
import jwt

from models.users import UserForm, User
from infrastructure.repositories.user_repository import UserRepository
from settings import SETTINGS, log

oauth2_schema = OAuth2PasswordBearer(tokenUrl='api/auth')


class ApplicationUser:
    def __init__(self, db: UserRepository)->None:
        self._db = db

    def _convert_id(self, id:str)->ObjectId:
        try:
            return ObjectId(id)

        except Exception as e:
            raise HTTPException(400, 'Error en la solicitud')

    def _create_access_token(self, user, days=1):
        data = {
            'user_id': str(user['_id']),
            'username': user['email'],
            'exp': datetime.now() + timedelta(days=days)
        }
        return jwt.encode(data, SETTINGS.secret_key, algorithm='HS256')

    def _decode_access_token(self, token: str):
        try:
            return jwt.decode(token, SETTINGS.secret_key, algorithms=['HS256'])

        except Exception as e:
            log.error(e)
            return None

    def get_current_user(self, token: str = Depends(oauth2_schema)):
        data = self._decode_access_token(token)
        if not data:
            raise HTTPException(400, 'Error en la solicitud, token invalido')
        return self.retrieve_user_by_id(data['user_id'])

    def create_user(self, user: UserForm):
        usr = dict(user)
        exists_user = self._db.retrieve_user_by_email(usr['email'])

        if exists_user and not exists_user['delete']:
            raise HTTPException(400, 'El usuario ya está registrado')

        hash_pass = UserForm.hash_password(usr['password'])
        usr.update({'password': hash_pass})
        usr = User(**usr).__dict__
        
        if exists_user and exists_user['delete']:
            return self._db.update_user(exists_user['_id'], usr)
 
        return self._db.create_user(usr)

    def retrive_users(self):
        return self._db.retrieve_users()

    def retrieve_user_by_id(self, id:str):
        try:
            usr_id = self._convert_id(id)
        except InvalidId:
            raise HTTPException(400, 'Error en la solicitud')

        user = self._db.retrieve_user_by_id(usr_id)

        if not user:
            raise HTTPException(404, 'Usuario no encontrado')
        return user

    def update_user(self, id:str, data:dict):

        data = {key: value for key, value in data.items() if value}

        if 'email' in data:
            exists_user = self._db.retrieve_user_by_email(data['email'])
            if exists_user and str(exists_user['_id']) != id:
                raise HTTPException(404, 'No se puede actualizar el email')
        usr_id = self._convert_id(id)
        return self._db.update_user(usr_id, data)

    def soft_delete_user(self, id:str):
        data = {
            'delete': True,
            'deleted_at': datetime.now()
        }
        usr_id = self._convert_id(id)
        _ = self._db.update_user(usr_id, data)

    def authenticate_user(self, username:str, password:str):
        user = self._db.retrieve_user_by_email(username)
        if not user:
            raise HTTPException(401, 'Usuario o password incorrectos')

        if user['password'] != UserForm.hash_password(password):
            raise HTTPException(
                401,
                'Usuario o password incorrectos',
                {'WWW-Authenticate': 'Beraer'}
            )
        
        try:

            self.update_user(user['_id'], {'last_login': datetime.now()})
        
        except Exception as e:
            log.error(f'Error autenticado usuario{e}')

        return {
            'access_token': self._create_access_token(user)
        }

    def delete(self, id:str):
        usr_id = self._convert_id(id)
        delete = self._db.delete_user(usr_id)
        if not delete:
            raise HTTPException(400, 'El usuario no existe')

