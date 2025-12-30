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
  
  if abs(error0 - 1.0) > 1e-6:
    new_ne00p = solution["ne00p"] - error0 / (error0 - 1.0) * solution["ne00p"]
    solution["ne00p"] = max(1e-6, new_ne00p)

  try:
    # DEBUG: Check error at bracket endpoints
    err_low = _adapted_errorfcn2(data, solution, 0.1 * np.asarray(solution["phi"]))
    err_high = _adapted_errorfcn2(data, solution, 10.0 * np.asarray(solution["phi"]))
    print(f"DEBUG: Solver scaling error check: f(0.1)={err_low}, f(10.0)={err_high}")

    # Use bounded search to prevent sign flipping or explosion of phi
    # Bracket [0.1, 10.0] restricts scaling to reasonable magnitude changes
    result = root_scalar(lambda factor: _adapted_errorfcn2(data, solution, factor * np.asarray(solution["phi"])), bracket=[0.1, 10.0], method="brentq")
    if result.converged:
      solution["phi"] = np.asarray(solution["phi"]) * result.root
      print(f"DEBUG: Solver scaling converged: factor={result.root}")
  except Exception as e:
    print(f"DEBUG: Solver scaling failed: {e}")
    pass

  for i in range(npoints - 2, 0, -1):
    try:
      result = root_scalar(lambda phii: _adapted_errorfcn(data, solution, phii, i), bracket=phibracket)
      if result.converged:
        phi_array = np.asarray(solution["phi"], dtype=float)
        # Apply damping to suppress high-frequency oscillations
        damping = 0.5
        phi_array[i] = (1.0 - damping) * phi_array[i] + damping * result.root
        solution["phi"] = phi_array
    except Exception:
      continue

  solution["errorfcn"] = errorfcn(data, solution)
  return solution

