from pydantic import Field

from .base_validator import ShapeBase


class PlaneValidator(ShapeBase):

    width: float = Field(gt=0, default=2)
    depth: float = Field(gt=0, default=2)
    segs_w: int = Field(gt=1, default=6)
    segs_d: int = Field(gt=1, default=6)
