from pydantic import BaseModel, ConfigDict, Field


class AbstractDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True
    )


class PaginationDTO(AbstractDTO):
    offset: int = Field(0, ge=0)
    limit: int = Field(10, le=10)
