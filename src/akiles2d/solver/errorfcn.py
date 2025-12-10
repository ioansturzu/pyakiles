"""Translation of ``+akiles2d/+solver/errorfcn.m``."""

from __future__ import annotations

import numpy as np

from ..simrc import Data
from ..electrons import parabolic as epar
from ..ions import parabolic as ipar


def errorfcn(data: Data, solution: dict[str, object], ierr: np.ndarray | list[int] | None = None) -> np.ndarray:
  """Compute quasineutrality and current/``phi_∞`` errors.

  Args:
    data: Simulation configuration.
    solution: Mapping with fields ``h``, ``r``, ``phi``, ``ne00p``, and
      ``npoints``.
    ierr: Optional indices of the error vector to compute. Defaults to all
      points.

  Returns:
    Array of error components with the same length as ``ierr``.
  """

  npoints = int(solution["npoints"])
  h = np.asarray(solution["h"], dtype=float)
  r = np.asarray(solution["r"], dtype=float)
  phi = np.asarray(solution["phi"], dtype=float)
  ne00p = float(solution.get("ne00p", 0.0))

  if ierr is None:
    ierr = np.arange(1, npoints + 1)
  ierr_arr = np.asarray(ierr) - 1

  electrons_moment = epar.semimaxwellian.moment(data, solution, 0, 0, 0, ierr_arr + 1)[0]
  ions_moment = ipar.cold.moment(data, solution, 0, 0, 0, ierr_arr + 1)[0]
  error_vec = 1 - electrons_moment / ions_moment

  infinity_mask = ierr_arr == (npoints - 1)
  if data.solver.errorfcn == "netcurrent" and infinity_mask.any():
    jze = epar.semimaxwellian.moment(data, solution, 1, 0, 0, [1])[0]
    jzi = ipar.cold.moment(data, solution, 1, 0, 0, [1])[0]
    error_vec[infinity_mask] = jzi - jze - data.solver.netcurrent
  elif data.solver.errorfcn == "phiinfty" and infinity_mask.any():
    error_vec[infinity_mask] = phi[npoints - 1] - data.solver.phiinfty

  return np.asarray(error_vec, dtype=float)

