import numpy as np
import pytest
from panda3d.core import Point3 

from shapes.polyhedron.polyhedron import TriangleGenerator


class TestTriangleGenerator:

    def setup_class(self):
        self.tri_generator = TriangleGenerator()

    @pytest.mark.parametrize(
        "tri", [
            ([np.array([0.0, 1.0, 0.5]), np.array([2.0, 4.0, 2.5]), np.array([5.0, -2.0, -1])]), ]
    )
    def test_calc_midpoint(self, tri):
        result = [p for p in self.tri_generator.calc_midpoints(tri)]
        print(result)

