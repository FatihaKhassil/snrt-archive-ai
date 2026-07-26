from fastapi import APIRouter

from app.schemas.rag_schema import RagRequest
from app.services.rag_service import RagService


router = APIRouter(

    prefix="/rag",

    tags=["RAG"]

)

service = RagService()


@router.post(

    "/ask"

)

async def ask(

    request: RagRequest

):

    return await service.ask(

        request.question

    )