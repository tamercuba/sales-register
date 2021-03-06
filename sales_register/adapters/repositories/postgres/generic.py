from abc import ABC, abstractmethod
from typing import List

from shared.entities import Entity
from sqlalchemy import delete, orm, select, update
from sqlalchemy.sql.dml import Delete, Update
from sqlalchemy.sql.selectable import Select


class SQLAlchemySemantic(ABC):
    @property
    @abstractmethod
    def model(self):
        pass

    @property
    def _select(self) -> Select:
        return select(self.model)

    @property
    def _delete(self) -> Delete:
        return delete(self.model)

    @property
    def _update(self) -> Update:
        return update(self.model)


class PostgresRepository(SQLAlchemySemantic):
    @property
    def mapper(self):
        pass

    def __init__(self, Session: orm.sessionmaker):
        self._Session = Session

    def _run_get(self, query: Select) -> Entity:
        with self._Session() as session:
            result = session.execute(query).scalars().one_or_none()
            session.commit()

            return self.mapper.to_entity(result) if result else None

    def _run_delete(self, query: Delete) -> None:
        with self._Session() as session:
            session.execute(query)
            session.commit()

    def _run_new(self, entity: Entity) -> Entity:
        with self._Session() as session:
            model = self.mapper.to_model(entity)
            session.add(model)
            session.commit()
            return entity

    def _run_list(self, query: Select) -> List[Entity]:
        with self._Session() as session:
            result_raw = session.execute(query).scalars()

            return [self.mapper.to_entity(model) for model in result_raw]

    def _run_update(self, query: Delete) -> None:
        with self._Session() as session:
            session.execute(query)
            session.commit()
