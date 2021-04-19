from typing import Optional

from adapters.api.services import authenticate_service, update_sale_service
from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

router = APIRouter()


class Request(BaseModel):
    code: str
    value: float
    date: str
    status: Optional[str]


class Response(Request):
    id: str


@router.put(
    '/sale/{sale_id}',
    status_code=status.HTTP_200_OK,
    response_model=Response,
)
def update_sale(
    sale_id: str, request: Request, auth: AuthJWT = Depends()
) -> Response:
    user = authenticate_service(auth)
    result = update_sale_service.handle(
        {
            'sale_id': sale_id,
            'salesman': user,
            'sale': {
                'code': request.code,
                'value': request.value,
                'date': request.date,
                'status': request.status,
            },
        }
    )

    return Response(
        **{
            'id': result.id,
            'code': result.code,
            'value': result.value,
            'date': str(result.date),
            'status': result.status,
        }
    )
