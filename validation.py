import re
from pydantic import BaseModel, Field, ConfigDict


class ConeModel(BaseModel):

    height: float = Field(gt=0, error_messages='')
    segs_c: int = Field(ge=3)
    segs_a: int = Field(ge=1)
    segs_bottom_cap: int = Field(alias="segs_bc", ge=0)
    segs_top_cap: int = Field(alias="segs_tc", ge=0)
    slice_deg: float = Field(ge=0, le=360)
    bottom_radius: float = Field(gt=0)
    top_radius: float = Field(ge=0)
    bottom_inner_radius: float = Field(ge=0)
    top_inner_radius: float = Field(ge=0)
    slice_caps_radial: int = Field(ge=0)
    slice_caps_axial: int = Field(ge=0)
    invert: bool

    model_config = ConfigDict(
        populate_by_name=True
    )



class RegexEqual(str):

    def __init__(self, string, sep='_'):
        self.string = string
        self.sep = sep

    def __eq__(self, pattern):
        match = re.search(pattern, self.string)
        return match is not None


def validate(name, value):
    msg = None

    match RegexEqual(name):

        case '^segs_[crsh]$':
            if type(value) is int and value >= 3:
                return
            msg = 'must be integer. minimum is 3'

        case '^segs_[v]$':
            if type(value) is int and value >= 2:
                return
            msg = 'must be integer. minimum is 2'

        case '^segs_[awdz]$':
            if type(value) is int and value >= 1:
                return
            msg = 'must be integer. minimum is 1'

        case '^segs_':
            if type(value) is int and value >= 0:
                return
            msg = 'must be integer and more than 0'

        case '_deg$':
            if 0 <= value <= 360:
                return
            msg = 'must be in the range from 0 to 360'

        case '^delta_radius$':
            if value < 0:
                return
            msg = 'top radius must be smaller than bottom radius'

        case '(_|^)inner_radius$' | '^top_radius$':
            if value >= 0:
                return
            msg = 'must be greater than or equal to 0'

        case '(_|^)radius$' | '_axis&':
            if value > 0:
                return
            msg = 'must be greater than 0'

        case '(_|^)thickness$':
            if value >= 0:

                return
            msg = 'inner radius must be in the range from 0 to radius'

        case '^invert$' | '^open_' | '^rounded_' | '_hemisphere$':
            if isinstance(value, bool):
                return
            msg = 'must be bool'

        case '^(height|width|depth)$':
            if value > 0:
                return
            msg = 'must be greater than 0'

        case '_clip$':
            if -1 <= value <= 1:
                return
            msg = f'must be -1 <= {name} <= 1'

    if msg:
        raise ValueError(f'{name}: {msg}.')