from pydantic import field_validator, ValidationInfo, Field
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails


from .base_validator import ShapeBase


class ConeValidator(ShapeBase):

    height: float = Field(gt=0, default=2.0)
    segs_c: int = Field(ge=3, default=40)
    segs_a: int = Field(ge=1, default=2)
    segs_bottom_cap: int = Field(alias="segs_bc", ge=0, default=2)
    segs_top_cap: int = Field(alias="segs_tc", ge=0, default=2)
    slice_deg: float = Field(ge=0, le=360, default=0.0)
    bottom_radius: float = Field(gt=0, default=1.0)
    top_radius: float = Field(ge=0, default=0.0)
    bottom_inner_radius: float = Field(ge=0, default=0.0)
    top_inner_radius: float = Field(ge=0, default=0.0)
    slice_caps_radial: int = Field(ge=0, alias='segs_sc_r', default=2)
    slice_caps_axial: int = Field(ge=0, alias='segs_sc_a', default=2)
    invert: bool = False

    @field_validator('bottom_inner_radius', 'top_inner_radius', mode='after')
    @classmethod
    def validate_inner_radius(cls, v: float, info: ValidationInfo):
        target_name = info.field_name.replace('inner_', '')

        if target_name in info.data and v > info.data[target_name]:
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    f'must be {info.field_name} <= {target_name}'
                ),
                loc=(info.field_name,),
                input=v,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )

        return v