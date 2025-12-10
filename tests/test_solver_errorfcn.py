import numpy as np

from akiles2d.simrc import simrc
from akiles2d.solver import errorfcn


def test_errorfcn_length():
  data = simrc()
  data.ions.mu = 10
  solution = {
    "h": np.array([1.0, 2.0]),
    "r": np.array([0.0, 0.0]),
    "phi": np.array([0.0, -0.5]),
    "ne00p": data.guess.ne00p,
    "npoints": 2,
  }
  err = errorfcn(data, solution)
  assert err.shape[0] == solution["npoints"]

