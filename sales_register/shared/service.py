from abc import ABC
from typing import Generic

from shared.ports import IRequest, IResponse


class IService(ABC, Generic[IRequest, IResponse]):
    def handle(self, request: IRequest) -> IResponse:
        pass