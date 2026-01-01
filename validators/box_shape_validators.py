from pydantic import field_validator, ValidationInfo, Field
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails

from .base_validator import ShapeBase


class BoxBaseValidator(ShapeBase):

    @field_validator('thickness', check_fields=False, mode='after')
    @classmethod
    def validate_thickness(cls, thickness: float, info: ValidationInfo):
        keys = ('width', 'depth', 'height')

        if all(k in info.data for k in keys) and thickness > 0:
            if thickness * 2 >= min(info.data[k] for k in keys):
                error_details = InitErrorDetails(
                    type=PydanticCustomError(
                        'value_error',
                        f'must be thickness x 2 < min({list(keys)})'
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


class BoxValidator(BoxBaseValidator):

    width: float = Field(gt=0, default=1.0)
    depth: float = Field(gt=0, default=1.0)
    height: float = Field(gt=0, default=1.0)
    segs_w: int = Field(gt=1, default=4)
    segs_d: int = Field(gt=1, default=4)
    segs_z: int = Field(gt=1, default=4)
    thickness: float = Field(ge=0, default=0.0)
    open_left: bool = False
    open_right: bool = False
    open_back: bool = False
    open_front: bool = False
    open_bottom: bool = False
    open_top: bool = False
    invert: bool = False


class RoundedBoxValidator(BoxBaseValidator):

    @field_validator('corner_radius', check_fields=False, mode='after')
    @classmethod
    def validate_corner_radius(cls, corner_radius: float, info: ValidationInfo):
        keys = ['width', 'depth']

        if (cls_name := cls.__name__) == 'RoundedEdgeBoxValidator':
            keys.append('height')

        if all(k in info.data for k in keys) and \
                corner_radius * 2 >= min([info.data[k] for k in keys]):
            error_details = InitErrorDetails(
                type=PydanticCustomError(
                    'value_error',
                    f'must be corner_radius x 2 < min({keys})'
                ),
                loc=('corner_radius',),
                input=corner_radius,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls_name,
                line_errors=[error_details]
            )

        return corner_radius

    @field_validator('thickness', check_fields=False, mode='after')
    @classmethod
    def validate_thickness(cls, thickness: float, info: ValidationInfo):
        if 'corner_radius' in info.data:
            if info.data['corner_radius'] == 0:
                return super().validate_thickness(thickness, info)

            if thickness > info.data['corner_radius']:
                error_details = InitErrorDetails(
                    type=PydanticCustomError(
                        'value_error',
                        'must be thickness <= corner_radius'),
                    loc=('thickness',),
                    input=thickness,
                    ctx={}
                )

                raise ValidationError.from_exception_data(
                    title=cls.__name__,
                    line_errors=[error_details]
                )

        return thickness


class RoundedCornerBoxValidator(RoundedBoxValidator):

    width: float = Field(gt=0, default=2.0)
    depth: float = Field(gt=0, default=2.0)
    height: float = Field(gt=0, default=2.0)
    segs_w: int = Field(gt=1, default=4)
    segs_d: int = Field(gt=1, default=4)
    segs_z: int = Field(gt=1, default=4)
    corner_radius: float = Field(ge=0, default=0.5)
    thickness: float = Field(ge=0, default=0.0)
    open_top: bool = False
    open_bottom: bool = False
    rounded_f_left: bool = True
    rounded_f_right: bool = True
    rounded_b_left: bool = True
    rounded_b_right: bool = True
    invert: bool = False


class RoundedEdgeBoxValidator(RoundedBoxValidator):

    width: float = Field(gt=0, default=2.0)
    depth: float = Field(gt=0, default=2.0)
    height: float = Field(gt=0, default=2.0)
    segs_w: int = Field(gt=1, default=4)
    segs_d: int = Field(gt=1, default=4)
    segs_z: int = Field(gt=1, default=4)
    corner_radius: float = Field(ge=0, default=0.5)
    thickness: float = Field(ge=0, default=0.0)
    open_top: bool = False
    open_bottom: bool = False
    invert: bool = False
