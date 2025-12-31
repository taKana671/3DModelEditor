from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails


class ShapeBase(BaseModel):

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        extra='ignore'
    )


class InnerRadiusValidator(ShapeBase):

    @field_validator('inner_radius', check_fields=False, mode='after')
    @classmethod
    def validate_inner_radius(cls, inner_radius: float, info: ValidationInfo):
        # I used field_validator instead of model_validator to show validation errors
        # on both model-level and field-level. I could not find how to do so by using model_validator.
        if 'radius' in info.data and inner_radius > info.data['radius']:
            error_details = InitErrorDetails(
                type=PydanticCustomError('value_error', 'must be inner_radius <= radius'),
                loc=('inner_radius',),
                input=inner_radius,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )

        return inner_radius


class SphericalValidator(InnerRadiusValidator):

    @field_validator('top_clip', check_fields=False, mode='after')
    @classmethod
    def validate_top_clip(cls, top_clip: float, info: ValidationInfo):
        if 'bottom_clip' in info.data and top_clip < info.data['bottom_clip']:
            error_details = InitErrorDetails(
                type=PydanticCustomError('value_error', 'must be top_clip >= bottom_clip'),
                loc=('top_clip',),
                input=top_clip,
                ctx={}
            )

            raise ValidationError.from_exception_data(
                title=cls.__name__,
                line_errors=[error_details]
            )
        return top_clip


class RoundedBoxValidator(ShapeBase):

    @field_validator('corner_radius', check_fields=False, mode='after')
    @classmethod
    def validate_corner_radius(cls, corner_radius: float, info: ValidationInfo):
        error_details = []
        keys = ['width', 'depth']

        if (cls_name := cls.__name__) == 'RoundedEdgeBoxValidator':
            keys.append('height')

        if all(k in info.data for k in keys):

            if corner_radius * 2 >= min([info.data[k] for k in keys]):
                error_details.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            'value_error',
                            f'must be corner_radius x 2 < min({keys})'
                        ),
                        loc=('corner_radius',),
                        input=corner_radius,
                        ctx={}
                    )
                )

        if 'thickness' in info.data and corner_radius < info.data['thickness']:
            error_details.append(
                InitErrorDetails(
                    type=PydanticCustomError(
                        'value_error',
                        'must be corner_radius >= thickness'),
                    loc=('corner_radius',),
                    input=corner_radius,
                    ctx={}
                )
            )

        if error_details:
            raise ValidationError.from_exception_data(
                title=cls_name,
                line_errors=error_details
            )

        return corner_radius


# class EllipticalValidator(ShapeBase):

#     @field_validator('thickness', check_fields=False, mode='after')
#     @classmethod
#     def validate_thickness(cls, thickness: float, info: ValidationInfo):
#         error_details = []

#         if (cls_name := cls.__name__) == 'EllipsoidValidator':
#             if all(k in info.data for k in ('minor_axis', 'top_clip', 'bottom_clip')):
#                 half = info.data['minor_axis'] / 2

#                 if thickness * 2 > (info.data['top_clip'] - info.data['bottom_clip']) * half:
#                     error_details.append(
#                         InitErrorDetails(
#                             type=PydanticCustomError(
#                                 'value_error',
#                                 'must be thickness x 2 <= (top_clip - bottom_clip) x minor_axis / 2'
#                             ),
#                             loc=('thickness',),
#                             input=thickness,
#                             ctx={}
#                         )
#                     )

#         # if ('major_axis' in info.data and 'minor_axis' in info.data) and \
#         #         thickness * 2 > min(info.data['major_axis'], info.data['minor_axis']):
#         #     error_details.append(
#         #         InitErrorDetails(
#         #             type=PydanticCustomError(
#         #                 'value_error',
#         #                 'must be thickness x 2 <= min(major_axis, minor_axis)'
#         #             ),
#         #             loc=('thickness',),
#         #             input=thickness,
#         #             ctx={}
#         #         )
#         #     )

#         if error_details:
#             raise ValidationError.from_exception_data(
#                 title=cls_name,
#                 line_errors=error_details
#             )

#         return thickness
