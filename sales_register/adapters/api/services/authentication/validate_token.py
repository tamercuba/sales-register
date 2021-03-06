from adapters.api.services.authentication.user import User
from domain.ports.repositories import ISalesmanRepository
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from shared.exceptions import EntityNotFound


class ValidateTokenService:
    def __init__(self, user_repo: ISalesmanRepository):
        self._repo = user_repo

    def __call__(self, auth: AuthJWT = Depends()) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            auth.jwt_required()
            user_id = auth.get_jwt_subject()
        except JWTDecodeError:
            raise credentials_exception

        try:
            user = self._repo.get_by_id(user_id)
            return user
        except EntityNotFound:
            raise credentials_exception
