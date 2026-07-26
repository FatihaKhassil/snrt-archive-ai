from pydantic import BaseModel
from typing import Literal


class UserCreateRequest(BaseModel):

    first_name: str

    last_name: str

    email: str

    phone: str

    department: str

    role: Literal[
        "ADMIN",
        "DOCUMENTALIST",
        "SNRT_USER"
    ]