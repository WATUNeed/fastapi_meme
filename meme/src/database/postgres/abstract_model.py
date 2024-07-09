from datetime import date
from typing import List

from sqlalchemy import MetaData, Date, inspect, func
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AbstractModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[date] = mapped_column(Date, server_default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column(Date, server_onupdate=func.now(), nullable=True)
    deleted_at: Mapped[date] = mapped_column(Date, nullable=True)

    def __repr__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in self.to_dict().items())
        return f'{self.__class__.__name__}({attrs})'

    def to_dict(self, with_related: bool = False):
        result = {
            field.name: getattr(self, field.name)
            for field in self.__table__.c  # noqa
            if field.name not in ['created_at', 'updated_at', 'deleted_at']
        }
        if with_related:
            for key in inspect(self.__class__).relationships.keys():
                try:
                    related = getattr(self, key)
                    if isinstance(related, List):
                        result.update({key: [item.to_dict(with_related=with_related) for item in related]})
                    elif related is not None:
                        result.update({key: related.to_dict(with_related=with_related)})
                except MissingGreenlet:
                    pass
        return result


meta = MetaData()
