from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Header

from schemas.users import user_entity, users_entity
from models.users import UserForm, UserUpdate, User
from applications.users import ApplicationUser
from infrastructure.api_provider import ApiProvider
from infrastructure.repositories.user_repository import UserRepository
from models.common import Token

oauth2_schema = OAuth2PasswordBearer(tokenUrl='api/auth')

application_users = ApplicationUser(UserRepository('public', 'users'))
api_provider = ApiProvider()

user = APIRouter()

@user.get('/users', tags=['Users'], status_code=200)
async def retrieve_users(
    token: str = Depends(oauth2_schema),
    current_user: User = Depends(application_users.get_current_user)
):
    if current_user['role'] != 'admin':
        raise HTTPException(
            401,
            'Sin Autorización'
        )
    return users_entity(application_users.retrive_users())

@user.post('/users', tags=['Users'], status_code=201)
async def create_user(user: UserForm):
    return user_entity(application_users.create_user(user))

@user.get('/users/{id}', tags=['Users'], status_code=200)
async def retrieve_user(
        id:str,
        token: str = Depends(oauth2_schema),
        current_user = Depends(application_users.get_current_user)
):

    if id != str(current_user['_id']) and current_user['role'] != 'admin':
        raise HTTPException(
            401,
            'Sin Autorización'
        )

    if id == str(current_user['_id']):
        user = current_user
    else:
        user = application_users.retrieve_user_by_id(id)

    if user['role'] != 'admin':
        data = api_provider.retrieve_data(user['role'])
        print(data)
        user.update({'data': data})

    return user_entity(user)

@user.put('/users/{id}', tags=['Users'], status_code=200)
async def update_user(
    id:str, user:UserUpdate,
    token: str = Depends(oauth2_schema),
    current_user = Depends(application_users.get_current_user)
):
    if id != str(current_user['_id']):
        raise HTTPException(
            401,
            'Sin Autorización'
        )
    return user_entity(application_users.update_user(id, dict(user)))

@user.delete('/users/{id}', tags=['Users'], status_code=204)
async def delete_user(
    id:str,
    token: str = Depends(oauth2_schema),
    current_user = Depends(application_users.get_current_user)
):
    if id != str(current_user['_id']):
        raise HTTPException(
            401,
            'Sin Autorización'
        )
    else:
        application_users.soft_delete_user(id)


@user.post('/auth',tags=['Auth'], response_model=Token)
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    return application_users.authenticate_user(data.username, data.password)

