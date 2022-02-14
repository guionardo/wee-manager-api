from fastapi import APIRouter

router = APIRouter()


@router.get('/health', tags=['health'])
async def basic_health_check():
    return "OK"
