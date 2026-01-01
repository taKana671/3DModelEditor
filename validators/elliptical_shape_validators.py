from pydantic import field_validator, ValidationInfo, Field
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .base_validator import ShapeBase


class EllipticalPrismValidator(ShapeBase):

    major_axis: float = Field(gt=0, default=2.0)
    minor_axis: float = Field(gt=0, default=1.0)
    thickness: float = Field(ge=0, default=0.0)
    height: float = Field(gt=0, default=1.0)
    segs_c: int = Field(ge=3, default=40)
    segs_a: int = Field(ge=1, default=2)
    segs_top_cap: int = Field(alias='segs_tc', ge=0, default=3)
    segs_bottom_cap: int = Field(alias='segs_bc', ge=0, default=3)
    ring_slice_deg: float = Field(ge=0, le=360, default=0.0)
    slice_caps_radial: int = Field(alias='segs_sc_r', ge=0, default=2)
    slice_caps_axial: int = Field(alias='segs_sc_a', ge=0, default=2)
    invert: bool = False

    @field_validator('thickness', mode='after')
    @classmethod
    def validate_thickness(cls, thickness: float, info: ValidationInfo):
        # I used field_validator instead of model_validator to show validation errors on both model-level and field-level.
        # I could not find how to do so by using model_validator.
        if ('major_axis' in info.data and 'minor_axis' in info.data) and \
                thickness * 2 >= min(info.data['major_axis'], info.data['minor_axis']):
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    'must be thickness x 2 <= min(major_axis, minor_axis)'
                ),
                loc=('thickness',),
                input=thickness,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__class__.__name__,
                line_errors=[error_details]
            )
        return thickness


class EllipsoidValidator(ShapeBase):

    major_axis: float = Field(gt=0, default=2.0)
    minor_axis: float = Field(gt=0, default=1.0)
    segs_h: int = Field(ge=3, default=40)
    segs_v: int = Field(ge=3, default=40)
    bottom_clip: float = Field(ge=-1, le=1, default=-1)
    top_clip: float = Field(le=1, default=1)
    thickness: float = Field(ge=0, default=0.0)
    slice_deg: float = Field(ge=0, le=360, default=0.0)
    segs_top_cap: int = Field(alias='segs_tc', ge=0, default=3)
    segs_bottom_cap: int = Field(alias='segs_bc', ge=0, default=3)
    segs_slice_caps: int = Field(alias="segs_sc", ge=0, default=2)
    invert: bool = False

    @field_validator('thickness', mode='after')
    @classmethod
    def validate_thickness(cls, thickness: float, info: ValidationInfo):
        error_details = []

        # if ('major_axis' in info.data and 'minor_axis' in info.data) and \
        #         thickness * 2 > min(info.data['major_axis'], info.data['minor_axis']):
        #     error_details.append(
        #         InitErrorDetails(
        #             type=PydanticCustomError(
        #                 'value_error',
        #                 'must be thickness x 2 <= min(major_axis, minor_axis)'
        #             ),
        #             loc=('thickness',),
        #             input=thickness,
        #             ctx={}
        #         )
        #     )

        if all(k in info.data for k in ('major_axis', 'minor_axis', 'top_clip', 'bottom_clip')):
            half = min(info.data['major_axis'], info.data['minor_axis']) / 2

            if thickness * 2 >= (info.data['top_clip'] - info.data['bottom_clip']) * half:
                error_details.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            'value_error',
                            'must be thickness * 2 <= (top_clip - bottom_clip) * min(minor_axis, major_axis) / 2'
                        ),
                        loc=('thickness',),
                        input=thickness,
                        ctx={}
                    )
                )

        if error_details:
            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=error_details
            )

        return thickness