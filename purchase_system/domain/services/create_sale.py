from typing import TypedDict

from domain.entities import Sale, SaleDTO
from domain.ports.repositories import ISaleRepository
from shared.service import IService


class CreateSaleRequest(TypedDict):
    salesman: str
    sale: SaleDTO


class CreateSaleService(IService[CreateSaleRequest, Sale]):
    def __init__(
        self,
        sale_repository: ISaleRepository,
    ):
        self._sale_repo = sale_repository

    def handle(self, request: CreateSaleRequest) -> Sale:
        requisitor = request['salesman']
        new_sale = requisitor.new_sale(**request['sale'])

        return self._sale_repo.new(new_sale)
