from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class Admin_base(BaseModel):
    id_token: Optional[str]

    class Config:
        orm_mode = True
