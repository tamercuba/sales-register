import json

import requests
from adapters.repositories.web.config import API_URL, REQUEST_TOKEN
from shared.exceptions import EntityNotFound


class GetTotalCashback:
    def total_salesman_cashback(self, cpf: str) -> float:
        url = API_URL + cpf
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise EntityNotFound(
                'An error occured when fetching total cashback',
                info={'status_code': response.status_code, 'cpf': cpf},
            )

        value = json.loads(response.content)

        return value['body']['credit']

    @property
    def headers(self):
        return {'Authorization': REQUEST_TOKEN}
