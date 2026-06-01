from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=False,
        samesite="none",
        secure=True
    )
    return {"state": "success"}
