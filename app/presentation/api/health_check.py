from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_204_NO_CONTENT)
async def health_check() -> None:
    pass
