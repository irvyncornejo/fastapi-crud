from fastapi import FastAPI
from fastapi import APIRouter
from contextlib import asynccontextmanager

from routes.users import user
from applications.users import ApplicationUser
from models.users import UserForm
from infrastructure.repositories.user_repository import UserRepository
from settings import log, SETTINGS

@asynccontextmanager
async def startup(app: FastAPI):
    log.info('Iniciando base...')
    db = UserRepository(SETTINGS.users_db_name, SETTINGS.users_colecction_name)
    db.start_db()

    try:
        user = ApplicationUser(db=db)
        usr = UserForm(
            full_name = 'Admin Admin',
            email = SETTINGS.admin_email,
            password = SETTINGS.admin_password,
            role = 'admin',
        )
        user.create_user(usr)

    except Exception as e:
        log.error(f'Error con el inicio de la base {e}')

    yield

@asynccontextmanager
async def shutdown(app: FastAPI):
    log.info('Cerrando')
    yield


app = FastAPI(
    title='Creación de usuarios',
    description='Api con el objetivo de tener un CRUD de usuarios con FastAPI y MongoDB',
    version='1',
    lifespan=startup
)

api = APIRouter(prefix='/api')
api.include_router(user)
app.include_router(api)
