from fastapi import FastAPI
from fastapi import APIRouter
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from routes.users import user
from applications.users import ApplicationUser
from models.users import UserForm
from infrastructure.repositories.user_repository import UserRepository
from settings import log, SETTINGS

@asynccontextmanager
async def startup(app: FastAPI):
    log.info('Iniciando base...')
    log.info(SETTINGS.mongo_conn_str)
    db_name = 'test' if SETTINGS.env == 'TEST' else SETTINGS.db_name
    db = UserRepository(db_name, SETTINGS.users_colecction_name)
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



app = FastAPI(
    title='Creación de usuarios',
    description='Api con el objetivo de tener un CRUD de usuarios con FastAPI y MongoDB',
    version='1',
    lifespan=startup
)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

api = APIRouter(prefix='/api')
api.include_router(user)
app.include_router(api)
