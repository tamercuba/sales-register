import pytest
from adapters.repositories.in_memory_repo import SalesmanRepository
from domain.entities import Salesman
from domain.use_cases import CreateSalesmanRequest, CreateSalesmanUseCase
from shared.exceptions import RepeatedEntry


class TestCreateSalesman:
    @pytest.fixture(autouse=True)
    def injector(self, salesman_data):
        self.salesman_data = salesman_data
        self.salesman = Salesman(**self.salesman_data)
        repo = SalesmanRepository(initial_values=[self.salesman])
        self.use_case = CreateSalesmanUseCase(salesman_repository=repo)

    @pytest.mark.parametrize(
        'data',
        [
            (
                {
                    'cpf': '11111',
                    'name': 'a',
                    'email': 'a@gmail.com',
                    'password': 'a',
                }
            ),
            (
                {
                    'cpf': '22222',
                    'name': 'b',
                    'email': 'b@gmail.com',
                    'password': 'a',
                    'is_staff': True,
                }
            ),
            (
                {
                    'cpf': '33333',
                    'name': 'c',
                    'email': 'c@gmail.com',
                    'password': 'a',
                    'is_staff': False,
                }
            ),
            (
                {
                    'cpf': '44444',
                    'name': 'd',
                    'email': 'd@gmail.com',
                    'password': 'a',
                    'is_staff': None,
                }
            ),
        ],
    )
    def test_create_salesman(self, data):
        new_salesman = CreateSalesmanRequest(**data)

        result = self.use_case.handle(new_salesman)

        assert result['cpf'] == new_salesman['cpf']
        assert result['id']

    @pytest.mark.parametrize(
        'salesman',
        [
            (
                {
                    'cpf': '123',
                    'name': 'a',
                    'email': 'a@a.com',
                    'password': 'a',
                }
            ),
            (
                {
                    'cpf': '000',
                    'name': 'b',
                    'email': 'didico@flamengo.com',
                    'password': 'a',
                }
            ),
        ],
    )
    def test_create_repeated_salesman(self, salesman):
        with pytest.raises(RepeatedEntry):
            self.use_case.handle(salesman)

    def test_create_wrong_request(self):
        with pytest.raises(KeyError):
            self.use_case.handle(request={'a': 1})