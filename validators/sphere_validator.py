from pydantic import field_validator, ValidationInfo, Field
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .cylindrical_shape_validators import InnerRadiusValidator


class SphericalValidator(InnerRadiusValidator):

    @field_validator('top_clip', check_fields=False, mode='after')
    @classmethod
    def validate_top_clip(cls, top_clip: float, info: ValidationInfo):
        if 'bottom_clip' in info.data and top_clip < info.data['bottom_clip']:
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    'must be top_clip >= bottom_clip'),
                # loc=('top_clip',),
                input=top_clip,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )
        return top_clip


class SphereValidator(SphericalValidator):

    radius: float = Field(gt=0, default=1.0)
    inner_radius: float = Field(ge=0, default=0.0)
    bottom_clip: float = Field(ge=-1, lt=1, default=-1)
    top_clip: float = Field(le=1, default=1)
    slice_deg: float = Field(ge=0, le=360, default=0.0)
    segs_h: int = Field(ge=3, default=40)
    segs_v: int = Field(ge=2, default=40)
    segs_top_cap: int = Field(alias="segs_tc", ge=0, default=2)
    segs_bottom_cap: int = Field(alias="segs_bc", ge=0, default=2)
    segs_slice_caps: int = Field(alias="segs_sc", ge=0, default=2)
    invert: bool = False