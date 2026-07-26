from pydantic import BaseModel

from typing import List


class DocumentUpdateRequest(BaseModel):

    title: str

    summary: str

    keywords: List[str]