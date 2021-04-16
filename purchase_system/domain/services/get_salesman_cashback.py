from typing import TypedDict

from domain.ports.repositories import ISaleRepository, ISalesmanRepository
from shared.service import IService


class GetSalesmanCashbackRequest(TypedDict):
    salesman_id: str


class GetSalesmanCashbackResponse(TypedDict):
    cashback_total: float


class GetSalesmanCashback(
    IService[GetSalesmanCashbackRequest, GetSalesmanCashbackResponse]
):
    def __init__(
        self,
        sale_repository: ISaleRepository,
        salesman_repository: ISalesmanRepository,
    ):
        self._sale_repo = sale_repository
        self._salesman_repo = salesman_repository

    def handle(
        self, request: GetSalesmanCashbackRequest, **kwargs
    ) -> GetSalesmanCashbackResponse:
        salesman = self._salesman_repo.get_by_id(request['salesman_id'])
        return self._sale_repo.total_salesman_cashback(salesman.cpf)
