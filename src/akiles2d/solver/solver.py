"""Translation of ``+akiles2d/+solver/solver.m``."""

from __future__ import annotations

from typing import Dict

import numpy as np
from scipy.optimize import root_scalar

from .errorfcn import errorfcn
from ..simrc import Data


def _adapted_errorfcn(data: Data, solution: dict[str, object], phii: float, idx: int) -> float:
  trial = dict(solution)
  phi_copy = np.array(trial["phi"], dtype=float)
  phi_copy[idx] = phii
  trial["phi"] = phi_copy
  trial["npoints"] = int(phi_copy.size)
  return float(np.asarray(errorfcn(data, trial, [idx + 1])).item())


def _adapted_errorfcn2(data: Data, solution: dict[str, object], phi: np.ndarray) -> float:
  trial = dict(solution)
  trial["phi"] = phi
  trial["npoints"] = int(phi.size)
  return float(np.asarray(errorfcn(data, trial, [phi.size])).item())


def solver(data: Data, solution: Dict[str, object]) -> Dict[str, object]:
  """Perform one sweep of the nonlinear solver."""

  phibracket = data.solver.phibracket
  npoints = int(solution["npoints"])

  error0 = float(solution["errorfcn"][0])
  solution["ne00p"] = solution["ne00p"] - error0 / (error0 - 1.0) * solution["ne00p"]

  try:
    result = root_scalar(lambda factor: _adapted_errorfcn2(data, solution, factor * np.asarray(solution["phi"])), x0=1.0, x1=1.1)
    if result.converged:
      solution["phi"] = np.asarray(solution["phi"]) * result.root
  except Exception:
    pass

  for i in range(npoints - 2, 0, -1):
    try:
      result = root_scalar(lambda phii: _adapted_errorfcn(data, solution, phii, i), bracket=phibracket)
      if result.converged:
        phi_array = np.asarray(solution["phi"], dtype=float)
        phi_array[i] = result.root
        solution["phi"] = phi_array
    except Exception:
      continue

  solution["errorfcn"] = errorfcn(data, solution)
  return solution

