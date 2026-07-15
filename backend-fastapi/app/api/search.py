from fastapi import APIRouter, Query

from app.services.search_service import SearchService


router = APIRouter()

search_service = SearchService()


@router.get("/search")
async def search(

    keyword: str = Query(...)

):

    return await search_service.keyword_search(

        keyword

    )