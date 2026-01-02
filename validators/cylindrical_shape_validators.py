from pydantic import field_validator, Field, ValidationInfo
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .base_validator import ShapeBase


class InnerRadiusValidator(ShapeBase):

    @field_validator('inner_radius', check_fields=False, mode='after')
    @classmethod
    def validate_inner_radius(cls, inner_radius: float, info: ValidationInfo):
        # I used field_validator instead of model_validator to show the all of validation errors
        # on both model-level and field-level. I could not find how to do so by using model_validator.
        if 'radius' in info.data and inner_radius > info.data['radius']:
            error_details = InitErrorDetails(
                type=PydanticCustomError('value_error', 'must be inner_radius <= radius'),
                # loc=('inner_radius',),
                input=inner_radius,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )

        return inner_radius


class CylinderValidator(InnerRadiusValidator):

    radius: float = Field(gt=0, default=1.0)
    inner_radius: float = Field(ge=0, default=0.0)
    height: float = Field(gt=0, default=1.0)
    segs_c: int = Field(ge=3, default=40)
    segs_a: int = Field(ge=1, default=2)
    segs_top_cap: int = Field(alias="segs_tc", ge=0, default=3)
    segs_bottom_cap: int = Field(alias="segs_bc", ge=0, default=3)
    ring_slice_deg: float = Field(ge=0, le=360, default=0.0)
    slice_caps_radial: int = Field(ge=0, alias='segs_sc_r', default=4)
    slice_caps_axial: int = Field(ge=0, alias='segs_sc_a', default=4)
    start_slice_cap: bool = True
    end_slice_cap: bool = True
    invert: bool = False


class CapsuleValidator(InnerRadiusValidator):

    radius: float = Field(gt=0, default=1.0)
    inner_radius: float = Field(ge=0, default=0.0)
    height: float = Field(gt=0, default=1.0)
    segs_c: int = Field(ge=3, default=40)
    segs_a: int = Field(ge=1, default=2)
    ring_slice_deg: float = Field(ge=0, le=360, default=0.0)
    slice_caps_radial: int = Field(ge=0, alias='segs_sc_r', default=2)
    slice_caps_axial: int = Field(ge=0, alias='segs_sc_a', default=2)
    top_hemisphere: bool = True
    bottom_hemisphere: bool = True
    invert: bool = False
