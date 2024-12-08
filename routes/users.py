from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas.users import user_entity, users_entity
from models.users import UserForm, UserUpdate, User, AdminUserForm
from applications.users import ApplicationUser
from infrastructure.api_provider import ApiProvider
from infrastructure.repositories.user_repository import UserRepository
from models.common import Token
from . import permission_exception
from settings import SETTINGS
from infrastructure.email_notifications import EmailService

oauth2_schema = OAuth2PasswordBearer(tokenUrl='api/auth')
db_name = 'test' if SETTINGS.env == 'TEST' else SETTINGS.db_name
application_users = ApplicationUser(db=UserRepository(db_name, 'users'))
api_provider = ApiProvider()
email_service = EmailService()

user = APIRouter()

@user.get('/users', tags=['Users'], status_code=200, description='Este endpoint es solo para admins')
async def retrieve_users(
    token: str = Depends(oauth2_schema),
    current_user: User = Depends(application_users.get_current_user)
):

    if current_user['role'] != 'admin':
        raise permission_exception
    return users_entity(application_users.retrive_users())

@user.post('/users', tags=['Users'], status_code=201)
async def create_user(user: UserForm):
    if user.role == 'admin':
        raise permission_exception

    usr = application_users.create_user(user)
    if usr:
        email_service.send_email_with_template(
            usr['email'],
            1,
            {'name': usr['full_name']}        
        )
    return user_entity(usr)

@user.get('/users/{id}', tags=['Users'], status_code=200)
async def retrieve_user(
        id:str,
        token: str = Depends(oauth2_schema),
        current_user = Depends(application_users.get_current_user)
):

    if id != str(current_user['_id']) and current_user['role'] != 'admin':
        raise permission_exception

    if id == str(current_user['_id']):
        user = current_user
    else:
        user = application_users.retrieve_user_by_id(id)

    if user['role'] != 'admin':
        data = api_provider.retrieve_data(user['role'])
        user.update({'data': data})

    return user_entity(user)

@user.put('/users/{id}', tags=['Users'], status_code=200)
async def update_user(
    id:str, user:UserUpdate,
    token: str = Depends(oauth2_schema),
    current_user = Depends(application_users.get_current_user)
):
    if id != str(current_user['_id']):
        raise permission_exception
    return user_entity(application_users.update_user(id, dict(user)))

@user.delete('/users/{id}', tags=['Users'], status_code=204)
async def delete_user(
    id:str,
    token: str = Depends(oauth2_schema),
    current_user = Depends(application_users.get_current_user)
)->None:
    if id != str(current_user['_id']) and current_user['role'] != 'admin':
        raise permission_exception
    
    if current_user['role'] == 'admin':
        application_users.delete(id)
        return

    application_users.soft_delete_user(id)


@user.post('/auth',tags=['Auth'], response_model=Token)
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    return application_users.authenticate_user(data.username, data.password)


@user.get('/me', tags=['Users'])
def retrive_me(
    token: str = Depends(oauth2_schema),
    current_user = Depends(application_users.get_current_user)
):
    return user_entity(current_user)


@user.post('/admins', tags=['Admins'], status_code=201, description='Endpoint para crear Admins')
async def create_user_admin(
    user: AdminUserForm,
    token: str = Depends(oauth2_schema),
    current_user: User = Depends(application_users.get_current_user)
):

    if current_user['role'] != 'admin':
        raise permission_exception

    usr = application_users.create_user(user)

    return user_entity(usr)