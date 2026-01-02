from pydantic import field_validator, Field, ValidationInfo
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .base_validator import ShapeBase


class RightTriangularPrismValidator(ShapeBase):

    adjacent: float = Field(gt=0, default=1.0)
    opposite: float = Field(gt=0, default=2.0)
    inner_adjacent: float = Field(ge=0, default=0.0)
    inner_opposite: float = Field(ge=0, default=0.0)
    height: float = Field(gt=0, default=2.0)
    segs_a: int = Field(ge=1, default=2)
    segs_top_cap: int = Field(alias="segs_tc", ge=0, default=3)
    segs_bottom_cap: int = Field(alias="segs_bc", ge=0, default=3)
    slice_caps_radial: int = Field(alias="segs_sc_r", ge=0, default=2)
    slice_caps_axial: int = Field(alias="segs_sc_a", ge=0, default=1)
    invert: bool = False

    @field_validator('inner_adjacent', 'inner_opposite', mode='after')
    @classmethod
    def validate_inner(cls, v: float, info: ValidationInfo):
        target_name = info.field_name.replace('inner_', '')
        if target_name in info.data and v > info.data[target_name]:
            error_details = InitErrorDetails(
                PydanticCustomError(
                    'value_error',
                    f'must be {info.field_name} <= {target_name}'
                ),
                # loc=(info.field_name,),
                input=v,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=error_details
            )

        return v