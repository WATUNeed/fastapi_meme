from typing import TypeVar, Generic, Type, Any, List, Dict
from uuid import UUID

from sqlalchemy import update, select, func, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abc.exception import DomainNotFound
from src.domain.abc.model import AbstractModel
from src.domain.abc.dto import AbstractDTO


ModelType = TypeVar('ModelType', bound=AbstractModel)
GetDTOType = TypeVar('GetDTOType', bound=AbstractDTO)
CreateDTOType = TypeVar('CreateDTOType', bound=AbstractDTO)
UpdateDTOType = TypeVar('UpdateDTOType', bound=AbstractDTO)

ID = int | UUID | str


class AbstractDAO(Generic[ModelType, GetDTOType, CreateDTOType, UpdateDTOType]):
    model: Type[ModelType] = AbstractModel
    get_scheme: Type[GetDTOType] = GetDTOType
    create_scheme: Type[CreateDTOType] = CreateDTOType
    update_scheme: Type[UpdateDTOType] = UpdateDTOType

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CreateDTOType, **kwargs: Any) -> GetDTOType:
        query = insert(
            self.model
        ).returning(
            self.model
        ).values(
            **data.model_dump(exclude_none=True),
            **kwargs
        )
        result = await self.session.scalar(query)
        new_instance = self.get_scheme.model_validate(result)
        return new_instance

    async def update(self, data: UpdateDTOType, **kwargs: Any):
        query = update(
            self.model
        ).where(
            self.model.id.in_({data.id})
        ).values(
            **data.model_dump(
                exclude_none=True,
                exclude={'id'}
            ),
            **kwargs
        )
        await self.session.execute(query)

    async def deactivate(self, instance_id: ID):
        query = update(
            self.model
        ).where(
            self.model.id == instance_id
        ).values(
            {'deleted_at': func.now()}
        )

        await self.session.execute(query)

    async def get_list(self) -> List[GetDTOType]:
        query = select(self.model)
        result = await self.session.scalars(query)
        return [self.get_scheme.model_validate(item) for item in result]

    async def get_dto_by_id(self, instance_id: ID) -> GetDTOType:
        result = await self.session.get(self.model, instance_id)
        if result is None:
            raise DomainNotFound(self.__class__.__name__)
        return self.get_scheme.model_validate(result)

    async def get_model_by_id(self, instance_id: ID) -> ModelType:
        query = select(
            self.model
        ).where(
            self.model.id == instance_id
        ).limit(1)
        result = (await self.session.execute(query)).scalar_one_or_none()

        if result is None:
            raise DomainNotFound(self.__class__.__name__)
        return result

    async def update_list(self, data: List[Dict[str, Any]]):
        if len(data) < 1:
            return None
        await self.session.execute(update(self.model), data)

    async def create_list(self, data: List[Dict[str, Any]], with_returning: bool = True) -> List[GetDTOType]:
        if len(data) < 1:
            return []
        if not with_returning:
            await self.session.execute(insert(self.model), data)
            return []

        query = insert(self.model).returning(self.model, sort_by_parameter_order=True)
        result = await self.session.scalars(query, data)
        return [self.get_scheme.model_validate(instance) for instance in result]

    async def delete_list(self, ids: List[ID]):
        if len(ids) < 1:
            return None
        await self.session.execute(delete(self.model).where(self.model.id.in_(ids)))

    async def delete(self, id: ID):
        await self.session.execute(delete(self.model).where(self.model.id == id))