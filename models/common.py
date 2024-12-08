from typing import Union
from datetime import datetime
from pydantic import BaseModel

class Common(BaseModel):
    created_at: datetime = datetime.now()
    delete: bool = False
    deleted_at: Union[datetime, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

