"""Translation of ``+akiles2d/+ions/+parabolic/+cold/moment.m``."""

from __future__ import annotations

import numpy as np

from ....simrc import Data


def moment(data: Data, solution: dict[str, object], evz: int, evr: int, evtheta: int, ipoints: np.ndarray | list[int] | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
  """Compute ion distribution moments on the plume axis."""

  chi = float(data.ions.chi)
  mu = float(data.ions.mu)

  h = np.asarray(solution["h"], dtype=float)
  r = np.asarray(solution["r"], dtype=float)
  phi = np.asarray(solution["phi"], dtype=float)

  if ipoints is None or len(ipoints) == 0:
    ipoints_arr = np.arange(h.size) + 1
  else:
    ipoints_arr = np.asarray(ipoints)
  idx = ipoints_arr.astype(int) - 1

  moment_val = np.zeros(idx.size)
  moment1 = np.zeros(idx.size)
  moment2 = np.zeros(idx.size)
  moment4 = np.zeros(idx.size)

  if np.any(r[idx] != 0):
    raise ValueError("Ion moment computation only valid on plume axis (r==0)")

  uz = np.sqrt(chi**2 - (2 / mu**2) * phi[idx])
  ni = chi / (uz * h[idx] ** 2)

  if evr == 0 and evtheta == 0:
    moment_val = ni * uz**evz
  moment1 = moment_val.copy()
  return moment_val, moment1, moment2, moment4

