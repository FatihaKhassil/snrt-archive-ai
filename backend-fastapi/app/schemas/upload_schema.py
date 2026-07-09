from fastapi import UploadFile
from pydantic import BaseModel


class UploadSchema(BaseModel):
    file: UploadFile