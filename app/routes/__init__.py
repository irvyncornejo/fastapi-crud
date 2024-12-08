from fastapi import HTTPException
from fastapi import status

permission_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Sin permisos necesarios',
    headers={"WWW-Authenticate": "Bearer"}
)
