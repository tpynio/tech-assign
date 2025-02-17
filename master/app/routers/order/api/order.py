import logging
from fastapi import APIRouter, Request, Depends, HTTPException, status
from core.config import settings
from app.routers.order.schemas.order import RegisterOrderParams, RegisterOrderResponse
from core.dependecies.authUser import prefetch_auth_user
from core.database.models.user import User


log = logging.getLogger(__name__)
router = APIRouter(
    tags=["Orders"],
)


@router.post(
    "/register",
    response_model=RegisterOrderResponse,
)
async def register_order(
    request: Request,
    order: RegisterOrderParams,
):
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)
    if not session_id:
        log.error("User session_id is missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    response = RegisterOrderResponse(order_id=777)
    return response


@router.post("/test")
async def test_order(user: User = Depends(prefetch_auth_user)):
    print(f"WTF {user}")
    return {"message": f"{user.dict()}"}
