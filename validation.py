from pydantic import BaseModel, Field, ConfigDict, model_validator


class ShapeBase(BaseModel):

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        extra='ignore'
    )


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
    invert: bool


class CylinderValidator(ShapeBase):

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

    @model_validator(mode='after')
    def validate_inner_radius(self):
        if self.inner_radius > self.radius:
            raise ValueError('must be inner_radius <= radius.')
        return self


class CapsuleValidator(ShapeBase):

    radius: float = Field(gt=0, default=1.0)
    inner_radius: float = Field(ge=0, default=0.0)
    height: float = Field(gt=0, default=1.0)
    segs_c: int = Field(ge=3, default=40)
    segs_a: int = Field(ge=1, default=2)
    ring_slice_deg: float = Field(ge=0, le=360, default=0.0)
    slice_caps_radial: int = Field(ge=0, alias='segs_sc_r', default=2)
    slice_caps_axial: int = Field(ge=0, alias='segs_sc_a')
    top_hemisphere: bool = True
    bottom_hemisphere: bool = True
    invert: bool = False

    @model_validator(mode='after')
    def validate_capsule(self):
        if self.inner_radius > self.radius:
            raise ValueError('must be inner_radius <= radius.')

        return self


class SphereValidator(ShapeBase):

    radius: float = Field(gt=0, default=1.0)
    inner_radius: float = Field(ge=0, default=0.0)
    segs_h: int = Field(ge=3, default=40)
    segs_v: int = Field(ge=2, default=40)
    segs_top_cap: int = Field(alias="segs_tc", ge=0, default=2)
    segs_bottom_cap: int = Field(alias="segs_bc", ge=0, default=2)
    segs_slice_caps: int = Field(alias="segs_sc", ge=0, default=2)
    slice_deg: float = Field(ge=0, le=360, default=0.0)
    bottom_clip: float = Field(ge=-1, lt=1, default=-1)
    top_clip: float = Field(le=1, default=1)
    invert: bool = False

    @model_validator(mode='after')
    def validate_sphere(self):
        if self.inner_radius > self.radius:
            raise ValueError('must be inner_radius <= radius.')

        if self.top_clip < self.bottom_clip:
            raise ValueError('must be top_clip >= bottom_clip.')

        return self


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

    @model_validator(mode='after')
    def validate_torus(self):
        if self.section_inner_radius > self.section_radius:
            raise ValueError('must be section_inner_radius <= section_radius.')

        return self


class BoxValidator(ShapeBase):

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


class PlaneValidator(ShapeBase):

    width: int = Field(gt=0, default=2)
    depth: int = Field(gt=0, default=2)
    segs_w: int = Field(gt=1, default=6)
    segs_d: int = Field(gt=1, default=6)


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

    @model_validator(mode='after')
    def validate_elliptical_prism(self):
        if self.thickness * 2 > min(self.major_axis, self.minor_axis):
            raise ValueError('must be thickness x 2 <= min(major_axis, minor_axis).')

        return self


class RoundedCornerBoxValidator(ShapeBase):

    width: float = Field(gt=0, default=2.0)
    depth: float = Field(gt=0, default=2.0)
    height: float = Field(gt=0, default=2.0)
    segs_w: int = Field(gt=1, default=4)
    segs_d: int = Field(gt=1, default=4)
    segs_z: int = Field(gt=1, default=4)
    thickness: float = Field(ge=0, default=0.0)
    open_top: bool = False
    open_bottom: bool = False
    corner_radius: float = Field(ge=0, default=0.5)
    rounded_f_left: bool = True
    rounded_f_right: bool = True
    rounded_b_left: bool = True
    rounded_b_right: bool = True
    invert: bool = False

    @model_validator(mode='after')
    def validate_rounded_corner_box(self):
        if self.corner_radius * 2 > min(self.width, self.depth):
            raise ValueError('must be corner_radius x 2 <= min(width, depth).')

        if self.thickness > self.corner_radius:
            raise ValueError('must be thickness <= corner_radius.')

        return self


class RoundedEdgeBoxValidator(ShapeBase):

    width: float = Field(gt=0, default=2.0)
    depth: float = Field(gt=0, default=2.0)
    height: float = Field(gt=0, default=2.0)
    segs_w: int = Field(gt=1, default=4)
    segs_d: int = Field(gt=1, default=4)
    segs_z: int = Field(gt=1, default=4)
    thickness: float = Field(ge=0, default=0.0)
    corner_radius: float = Field(ge=0, default=0.5)
    open_top: bool = False
    open_bottom: bool = False
    invert: bool = False

    @model_validator(mode='after')
    def validate_rounded_edge_box(self):
        if self.corner_radius * 2 > min(self.width, self.depth, self.height):
            raise ValueError('must be corner_radius x 2 <= min(width, depth, self.heigh).')

        if self.thickness > self.corner_radius:
            raise ValueError('must be thickness <= corner_radius.')

        return self


class EllipsoidValidator(ShapeBase):

    major_axis: float = Field(gt=0, default=2.0)
    minor_axis: float = Field(gt=0, default=1.0)
    thickness: float = Field(ge=0, default=0.0)
    segs_h: int = Field(ge=3, default=40)
    segs_v: int = Field(ge=3, default=40)
    segs_top_cap: int = Field(alias='segs_tc', ge=0, default=3)
    segs_bottom_cap: int = Field(alias='segs_bc', ge=0, default=3)
    segs_slice_caps: int = Field(alias="segs_sc", ge=0, default=2)
    slice_deg: float = Field(ge=0, le=360, default=0.0)
    bottom_clip: float = Field(ge=-1, le=1, default=-1)
    top_clip: float = Field(le=1, default=1)
    invert: bool = False

    @model_validator(mode='after')
    def validate_ellipsoid(self):
        if self.thickness * 2 > min(self.major_axis, self.minor_axis):
            raise ValueError('must be thickness * 2 <= min(major_axis, minor_axis).')

        half = self.minor_axis / 2
        if self.thickness * 2 > (self.top_clip - self.bottom_clip) * half:
            raise ValueError('must be thickness * 2 <= (top_clip - bottom_clip) * minor_axis / 2.')

        if self.top_clip < self.bottom_clip:
            raise ValueError('must be top_clip >= bottom_clip.')

        return self