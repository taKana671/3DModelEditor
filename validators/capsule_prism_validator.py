from pydantic import field_validator, ValidationInfo, Field
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .base_validator import ShapeBase


class CapsulePrismValidator(ShapeBase):

    width: float = Field(gt=0, default=1.0)
    depth: float = Field(gt=0, default=1.0)
    height: float = Field(gt=0, default=1.0)
    segs_w: int = Field(gt=1, default=4)
    segs_d: int = Field(gt=1, default=4)
    segs_z: int = Field(gt=1, default=4)
    thickness: float = Field(ge=0, default=0.0)
    rounded_left: bool = True
    rounded_right: bool = True
    open_top: bool = False
    open_bottom: bool = False
    invert: bool = False

    @field_validator('thickness', mode='after')
    @classmethod
    def validate_thickness(cls, thickness: float, info: ValidationInfo):

        if 'depth' in info.data and thickness * 2 >= info.data['depth']:
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    'must be thickness x 2 < depth'
                ),
                loc=('thickness',),
                input=thickness,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )

        return thickness