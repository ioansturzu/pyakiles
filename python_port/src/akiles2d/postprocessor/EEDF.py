"""Translation of ``+akiles2d/+postprocessor/EEDF.m``."""

from __future__ import annotations

import numpy as np

from ..simrc import Data


def EEDF(data: Data, solution: dict[str, object]) -> dict[str, object]:
  """Compute the electron energy distribution function."""

  nintegrationpoints = np.asarray(data.electrons.nintegrationpoints, dtype=int)
  alpha = float(data.electrons.alpha)

  h = np.asarray(solution["h"], dtype=float).reshape(-1)
  r = np.asarray(solution["r"], dtype=float).reshape(-1)
  phi = np.asarray(solution["phi"], dtype=float).reshape(-1)
  ne00p = float(solution.get("ne00p", 0.0))
  npoints = h.size
  nEk = int(nintegrationpoints.sum())

  pperplimbwd = np.zeros((npoints, nEk))
  pperplimfwd = np.zeros((npoints, nEk))
  Ek = np.zeros((npoints, nEk))

  for ip in range(npoints):
    E_transition = 1.5 * (phi[ip] - phi[-1])
    if np.isinf(phi[-1]) or E_transition <= 0:
      E_transition = 5.0
    sep = E_transition / (nintegrationpoints[0] - 1)
    f = 1.05
    Ek[ip, : nintegrationpoints[0]] = np.linspace(0.0, E_transition, int(nintegrationpoints[0]))
    Ek[ip, nintegrationpoints[0] :] = E_transition + sep * (f ** np.arange(1, int(nintegrationpoints[1]) + 1) - 1) / (f - 1)
    if ip == npoints - 1:
      continue
    pperpmin = r[ip] ** 2 / (np.sqrt(2.0) * h[ip] ** 2)
    for iEk in range(nEk):
      pperp = (Ek[ip, iEk] + phi - phi[ip]) * h**2 / np.sqrt(2.0)
      pperplimbwd[ip, iEk] = max(pperpmin, np.min(pperp[: ip + 1]))
      pperplimfwd[ip, iEk] = max(pperpmin, np.min(pperp[ip:]))

  H = np.repeat(h.reshape(-1, 1), nEk, axis=1)
  PPERP = Ek * H**2 / np.sqrt(2.0)
  PPERPMIN = np.repeat((r**2 / (np.sqrt(2.0) * h**2)).reshape(-1, 1), nEk, axis=1)
  PHI = np.repeat(phi.reshape(-1, 1), nEk, axis=1)

  def G(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    return 2 * ne00p / np.sqrt(np.pi) * np.exp(PHI) * np.exp(-Ek) * (np.sqrt(np.maximum(0.0, Ek - np.sqrt(2.0) / H**2 * p1)) - np.sqrt(np.maximum(0.0, Ek - np.sqrt(2.0) / H**2 * p2)))

  solution.setdefault("electrons", {})
  solution["electrons"]["Ek"] = Ek
  solution["electrons"]["EEDF1"] = G(PPERPMIN, np.minimum(pperplimbwd, pperplimfwd))
  solution["electrons"]["EEDF2"] = 2 * np.maximum(0.0, G(pperplimfwd, pperplimbwd))
  solution["electrons"]["EEDF4"] = (1 + alpha) * np.maximum(0.0, G(np.maximum(pperplimbwd, pperplimfwd), PPERP))
  solution["electrons"]["EEDF"] = solution["electrons"]["EEDF1"] + solution["electrons"]["EEDF2"] + solution["electrons"]["EEDF4"]
  return solution

