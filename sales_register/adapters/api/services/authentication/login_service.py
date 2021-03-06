from typing import Optional

from adapters.api.services.authentication.user import User
from adapters.repositories.postgres.password_manager_interface import (
    IPasswordManager,
)
from domain.ports.repositories import ISalesmanRepository
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from shared.exceptions import EntityNotFound


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginService:
    def __init__(
        self, user_repo: ISalesmanRepository, hash_manager: IPasswordManager
    ):
        self._repo = user_repo
        self._hash_manager = hash_manager

    def __call__(self, request: LoginRequest) -> Optional[User]:
        try:
            user: User = self._repo.get_by_email(request.email)
            if self._hash_manager.validate_password(
                request.password, user.password.get_secret_value()
            ):
                return user

        except EntityNotFound:
            pass

        return None

    def create_access_token(self, user_id: str, auth: AuthJWT) -> str:
        return f'Bearer {auth.create_access_token(subject=user_id)}'
