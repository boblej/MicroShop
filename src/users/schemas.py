from pydantic import BaseModel, EmailStr
from typing import  Annotated
from annotated_types import  MaxLen, MinLen

class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(32), MinLen(3)]
    email: EmailStr
