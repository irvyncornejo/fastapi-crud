from enum import Enum
from datetime import date
import hashlib

from typing import Optional, Union
from pydantic import BaseModel, EmailStr, field_validator
from decimal import Decimal

from .common import Common

class Roles(str, Enum):
    admin = 'admin'
    films = 'films'
    people = 'people'
    locations = 'locations'
    species = 'species'
    vehicles = 'vehicles'

class User(Common):
    full_name: str
    email: EmailStr
    password: str
    role: Roles
    last_login: Union[date, None] = None
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None


class UserForm(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Roles

    @field_validator('password')
    def validate_password(cls, password):
        if len(password.strip()) < 5:
            raise ValueError('La contraseña debe tener al menos 5 caracteres')
        return password

    @field_validator('role')
    def validate_role(cls, value):
        if value not in Roles._member_names_:
            raise ValueError('Role invalido')
        return value

    @field_validator('full_name')
    def validatate_full_name(cls, full_name):
        if len(full_name) < 5 or len(full_name) > 60:
            raise ValueError('El valor de full_name debe estar entre 5 y 60')
        return full_name

    @classmethod
    def hash_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Luis López",
                "email": "luis@gmail.com",
                "role": 'films',
                "password": '#1979ER'
            }
        }

class UserUpdate(BaseModel):
    full_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    role: Union[Roles, None] = None

    @field_validator('role')
    def validate_role(cls, value):
        if value not in Roles._member_names_:
            raise ValueError('Role invalido')
        return value

    @field_validator('full_name')
    def validatate_full_name(cls, full_name):
        if len(full_name) < 5 or len(full_name) > 60:
            raise ValueError('El valor de full_name debe estar entre 5 y 60')
        return full_name
