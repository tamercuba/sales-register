import pytest
from adapters.repositories.in_memory_repo import SaleRepository
from domain.entities import Sale, Salesman, SaleStatus
from domain.use_cases import UpdateSaleUseCase, UpdateSaleUseCaseRequest
from domain.use_cases.exceptions import CantBeUpdated
from shared.exceptions import EntityNotFound


class TestUpdateSale:
    @pytest.fixture(autouse=True)
    def injector(self, sale_data, salesman_data):
        self.sale_data = sale_data
        self.sale = Sale(**self.sale_data)
        del self.sale_data['salesman_cpf']

        self.salesman_data = salesman_data
        self.salesman = Salesman(**self.salesman_data)

        self.sale_repo = SaleRepository(initial_values=[self.sale])

        self.use_case = UpdateSaleUseCase(sale_repository=self.sale_repo)

    def test_update_wrong_status(self):
        new_sale_data = {
            'code': 'a',
            'value': 10,
            'date': '1997-09-01',
            'salesman_cpf': '123',
            'status': SaleStatus.REPPROVED,
        }
        new_sale = Sale(**new_sale_data)

        self.sale_repo.new(new_sale)

        with pytest.raises(CantBeUpdated):
            self.use_case.handle(
                UpdateSaleUseCaseRequest(
                    **{
                        'sale_id': new_sale.id,
                        'salesman': self.salesman,
                        'sale': new_sale_data,
                    }
                )
            )

    def test_update_wrong_cpf(self):
        new_salesman_data = {**self.salesman_data, 'cpf': '456'}
        new_salesman = Salesman(**new_salesman_data)

        with pytest.raises(CantBeUpdated):
            self.use_case.handle(
                UpdateSaleUseCaseRequest(
                    **{
                        'sale_id': self.sale.id,
                        'salesman': new_salesman,
                        'sale': self.sale_data,
                    }
                )
            )

    def test_update_wrong_is_staff_with_wrong_cpf(self):
        new_salesman_data = {
            **self.salesman_data,
            'cpf': '789',
            'is_staff': True,
        }
        new_salesman = Salesman(**new_salesman_data)

        updated_sale_data = {**self.sale_data, 'code': 'B'}

        result = self.use_case.handle(
            UpdateSaleUseCaseRequest(
                **{
                    'sale_id': self.sale.id,
                    'salesman': new_salesman,
                    'sale': updated_sale_data,
                }
            )
        )

        assert result == self.sale
        assert result.model_dump() != self.sale.model_dump()

    def test_update_right_cpf(self):
        updated_sale_data = {**self.sale_data, 'code': 'B'}

        result = self.use_case.handle(
            UpdateSaleUseCaseRequest(
                **{
                    'sale_id': self.sale.id,
                    'salesman': self.salesman,
                    'sale': updated_sale_data,
                }
            )
        )

        assert result == self.sale
        assert result.model_dump() != self.sale.model_dump()

    def test_update_nonexistent_sale(self):
        updated_sale_data = {**self.sale_data, 'code': 'B'}

        with pytest.raises(EntityNotFound):
            self.use_case.handle(
                UpdateSaleUseCaseRequest(
                    **{
                        'sale_id': '93939393939393',
                        'salesman': self.salesman,
                        'sale': updated_sale_data,
                    }
                )
            )
