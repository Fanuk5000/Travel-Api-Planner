import httpx
from fastapi import HTTPException, status


async def validate_external_place(external_id: int) -> None:
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Place with external_id {external_id} not found in Art Institute API.",
            )
