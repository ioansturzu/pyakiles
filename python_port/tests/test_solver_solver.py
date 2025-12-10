import numpy as np

from akiles2d.solver import solver
from akiles2d.simrc import simrc


def test_solver_updates_phi():
  data = simrc()
  data.solver.phibracket = (-1.0, 0.1)
  solution = {
    "h": np.array([1.0, 2.0]),
    "r": np.array([0.0, 0.0]),
    "phi": np.array([0.0, -0.1]),
    "ne00p": data.guess.ne00p,
    "npoints": 2,
    "errorfcn": np.array([0.2, 0.1]),
  }
  updated = solver(data, solution)
  assert updated["phi"].shape[0] == solution["npoints"]

