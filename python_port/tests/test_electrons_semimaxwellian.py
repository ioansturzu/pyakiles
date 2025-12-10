import numpy as np

from akiles2d.electrons.parabolic import semimaxwellian
from akiles2d.simrc import simrc


def _sample_solution():
  data = simrc()
  solution = {
    "h": np.array([1.0, 2.0]),
    "r": np.array([0.0, 0.0]),
    "phi": np.array([0.0, -1.0]),
    "ne00p": data.guess.ne00p,
    "npoints": 2,
  }
  return data, solution


def test_moment_trivial():
  data, solution = _sample_solution()
  moment, _, _, _ = semimaxwellian.moment(data, solution, 0, 1, 0)
  assert np.all(moment == 0)


def test_ne00p_phiinfty_signs():
  ne00p, phiinfty = semimaxwellian.ne00p_phiinfty_nobarriers(0.02)
  assert phiinfty < 0
  assert ne00p > 0

