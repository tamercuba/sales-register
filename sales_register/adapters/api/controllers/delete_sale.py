from adapters.api.services import (
    DeleteSaleUseCaseRequest,
    delete_sale_use_case,
    validate_token_service,
)
from adapters.api.services.authentication import User
from fastapi import APIRouter, Depends, Response, status

router = APIRouter()


@router.delete('/sale/{sale_id}')
def delete_sale(sale_id: str, user: User = Depends(validate_token_service)):
    delete_sale_use_case.handle(
        DeleteSaleUseCaseRequest(**{'sale_id': sale_id, 'salesman': user})
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
