import numpy as np
import pytest

from akiles2d.ions.parabolic import cold
from akiles2d.simrc import simrc


def test_moment_axis():
  data = simrc()
  data.ions.mu = 10
  solution = {"h": np.array([1.0, 1.5]), "r": np.array([0.0, 0.0]), "phi": np.array([0.0, -0.2])}
  moment, _, _, _ = cold.moment(data, solution, 0, 0, 0)
  assert moment.shape == (2,)
  assert moment[0] > 0


def test_off_axis_error():
  data = simrc()
  solution = {"h": np.array([1.0, 1.5]), "r": np.array([0.0, 0.1]), "phi": np.array([0.0, -0.2])}
  with pytest.raises(ValueError):
    cold.moment(data, solution, 0, 0, 0)

