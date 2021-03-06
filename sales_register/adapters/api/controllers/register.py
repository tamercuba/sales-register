from adapters.api.services import (
    CreateSalesmanUseCaseRequest,
    create_salesman_use_case,
    login_service,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from shared.exceptions import RepeatedEntry

router = APIRouter()


class Request(CreateSalesmanUseCaseRequest):
    pass


class Response(BaseModel):
    access_token: str


@router.post(
    '/register', status_code=status.HTTP_201_CREATED, response_model=Response
)
def register(request: Request, auth: AuthJWT = Depends()):
    try:
        user = create_salesman_use_case.handle(request)
        token = login_service.create_access_token(user.id, auth)
        return Response(access_token=token)

    except RepeatedEntry as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.info
        )
