from pydantic import BaseModel, ConfigDict


class ShapeBase(BaseModel):

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        extra='ignore'
    )