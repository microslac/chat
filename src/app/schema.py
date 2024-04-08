from typing import List
from pydantic import BaseModel, ConfigDict
from app.database import Base


class SchemaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def dump(
        cls, instance: List[Base] | Base, /, many: bool = False, **kwargs
    ) -> List[dict] | dict:
        def dump(ins):
            return cls.model_validate(ins).model_dump(**kwargs)

        if many:
            return [dump(ins) for ins in instance]
        return dump(instance)


class ResponseOut(BaseModel):
    ok: bool = True
