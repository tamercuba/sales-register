from typing import TypedDict

from domain.entities import Salesman
from domain.ports.repositories import ISalesmanRepository
from shared.exceptions import RepeatedEntry
from shared.service import IService


class CreateSalesmanRequest(TypedDict):
    cpf: str
    name: str
    email: str
    password: str


class CreateSalesmanResponse(CreateSalesmanRequest):
    id: str


class CreateSalesman(IService[CreateSalesmanRequest, CreateSalesmanResponse]):
    def __init__(self, salesman_repository: ISalesmanRepository):
        self._repo = salesman_repository

    def handle(
        self, request: CreateSalesmanRequest, **kwargs
    ) -> CreateSalesmanResponse:
        existing_salesman = self._repo.get_by_cpf(request['cpf'])
        if existing_salesman:
            raise RepeatedEntry(
                'This salesman already exists', _id=existing_salesman.id
            )

        new_salesman = Salesman(**request)
        self._repo.new(new_salesman)
        response: CreateSalesmanResponse = self.get_response(new_salesman)

        return response

    def get_response(self, salesman: Salesman) -> CreateSalesmanResponse:
        return {
            'id': salesman.id,
            'cpf': salesman.cpf,
            'name': salesman.name,
            'email': salesman.email,
            'password': salesman.password,
        }