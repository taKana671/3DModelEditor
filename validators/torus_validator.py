from pydantic import field_validator, Field, ValidationInfo
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .base_validator import ShapeBase


class TorusValidator(ShapeBase):

    segs_r: int = Field(ge=3, default=40)
    segs_s: int = Field(ge=3, default=20)
    ring_radius: float = Field(gt=0, default=1.0)
    section_radius: float = Field(gt=0, default=0.5)
    section_inner_radius: float = Field(ge=0, default=0.0)
    ring_slice_deg: float = Field(ge=0, le=360, default=0.0)
    section_slice_deg: float = Field(ge=0, le=360, default=0.0)
    section_slice_start_cap: int = Field(alias='segs_sssc', ge=0, default=2)
    section_slice_end_cap: int = Field(alias='segs_ssec', ge=0, default=2)
    ring_slice_start_cap: int = Field(alias='segs_rssp', ge=0, default=2)
    ring_slice_end_cap: int = Field(alias='segs_rsec', ge=0, default=2)
    invert: bool = False

    @field_validator('section_radius', mode='after')
    @classmethod
    def validate_ring_radius(cls, section_radius: float, info: ValidationInfo):
        error_details = []

        if 'ring_radius' in info.data and section_radius > info.data['ring_radius']:
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    'section_radius <= ring_radius'
                ),
                # loc=('ring_radius',),
                input=section_radius,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )

        return section_radius

    @field_validator('section_inner_radius', mode='after')
    @classmethod
    def validate_section_inner_radius(cls, section_inner_radius: float, info: ValidationInfo):
        if 'section_radius' in info.data and \
                section_inner_radius > info.data['section_radius']:
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    'section_inner_radius <= section_radius'
                ),
                # loc=('section_inner_radius',),
                input=section_inner_radius,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )

        return section_inner_radius