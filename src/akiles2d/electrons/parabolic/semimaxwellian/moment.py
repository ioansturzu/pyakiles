"""Translation of ``+akiles2d/+electrons/+parabolic/+semimaxwellian/moment.m``."""

from __future__ import annotations

import numpy as np
from scipy.special import gamma, gammainc, gammaincc

from ....simrc import Data


def _prepare_energy_grid(phi_slice: np.ndarray, h_slice: np.ndarray, r_slice: np.ndarray, ip: int, nintegration: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
  nE = int(nintegration.sum())
  E_grid = np.zeros(nE)
  E_transition = 1.5 * (phi_slice[ip] - phi_slice[-1])
  if np.isinf(phi_slice[-1]) or E_transition <= 0:
    E_transition = 5.0
  sep = E_transition / (nintegration[0] - 1)
  f = 1.05
  E_grid[: nintegration[0]] = np.linspace(0.0, E_transition, int(nintegration[0]))
  E_grid[nintegration[0] :] = E_transition + sep * (f ** np.arange(1, int(nintegration[1]) + 1) - 1) / (f - 1)

  pperp_limbwd = np.zeros(nE)
  pperp_limfwd = np.zeros(nE)
  if ip == len(phi_slice) - 1:
    return E_grid, pperp_limbwd, pperp_limfwd

  for idx in range(nE):
    denom = h_slice[ip] ** 2 / h_slice**2 - 1
    with np.errstate(divide="ignore", invalid="ignore"):
      pperp_vals = np.divide(E_grid[idx] + phi_slice - phi_slice[ip], denom, where=denom != 0)
    pperp_vals -= (r_slice[ip] ** 2) / h_slice[ip] ** 4
    pperp_vals[~np.isfinite(pperp_vals)] = np.nan

    backward = pperp_vals[: ip + 1]
    forward = pperp_vals[ip + 1 :]

    if np.isfinite(backward).any():
      pperp_limbwd[idx] = max(0.0, np.nanmin(backward))
    if np.isfinite(forward).any():
      pperp_limfwd[idx] = max(0.0, np.nanmax(forward))
  if ip == 0:
    pperp_limbwd[0] = np.inf
  return E_grid, pperp_limbwd, pperp_limfwd


def moment(data: Data, solution: dict[str, object], evz: int, evr: int, evtheta: int, ipoints: np.ndarray | list[int] | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
  """Compute electron distribution moments for the semimaxwellian model."""

  nintegrationpoints = np.asarray(data.electrons.nintegrationpoints, dtype=int)
  alpha = float(data.electrons.alpha)

  h = np.asarray(solution["h"], dtype=float).reshape(-1)
  r = np.asarray(solution["r"], dtype=float).reshape(-1)
  phi = np.asarray(solution["phi"], dtype=float).reshape(-1)
  ne00p = float(solution.get("ne00p", 0.0))
  npoints = h.size

  if ipoints is None or len(ipoints) == 0:
    ipoints_arr = np.arange(npoints) + 1
  else:
    ipoints_arr = np.asarray(ipoints)
  ipoints_zero = ipoints_arr.astype(int) - 1

  nipoints = ipoints_zero.size
  nE_total = int(nintegrationpoints.sum())

  moment1 = np.zeros(nipoints)
  moment2 = np.zeros(nipoints)
  moment4 = np.zeros(nipoints)
  moment_total = np.zeros(nipoints)

  if evr % 2 == 1 or evtheta % 2 == 1:
    return moment_total, moment1, moment2, moment4

  Hijk = lambda a, b: np.maximum(0.0, gamma((2 + evr + evtheta) / 2) * (gammainc((2 + evr + evtheta) / 2, b) - gammainc((2 + evr + evtheta) / 2, a)))

  def dGijk(E_a: np.ndarray, E_b: np.ndarray, G_a: np.ndarray, G_b: np.ndarray) -> np.ndarray:
    numerator = gamma((1 + evz) / 2) * (G_b * E_a - G_a * E_b) * (gammainc((1 + evz) / 2, E_b) - gammainc((1 + evz) / 2, E_a))
    numerator += gamma((3 + evz) / 2) * (G_a - G_b) * (gammainc((3 + evz) / 2, E_b) - gammainc((3 + evz) / 2, E_a))
    denom = E_a - E_b
    return numerator / denom

  factor_base = ne00p * 2 ** ((evz + evr + evtheta) / 2) * gamma((1 + evr) / 2) * gamma((1 + evtheta) / 2) / gamma(1 + (evr + evtheta) / 2) / np.pi ** 1.5
  factor_base *= np.exp(phi[ipoints_zero] - r[ipoints_zero] / h[ipoints_zero] ** 4)

  for idx, ip in enumerate(ipoints_zero):
    E_grid, pperp_limbwd, pperp_limfwd = _prepare_energy_grid(phi, h, r, ip, nintegrationpoints)
    H1 = Hijk(pperp_limfwd, pperp_limbwd)
    dG1 = dGijk(E_grid[:-1], E_grid[1:], H1[:-1], H1[1:])
    tail = H1[-1] * gamma((1 + evz) / 2) * gammaincc((1 + evz) / 2, E_grid[-1])
    moment1[idx] = factor_base[idx] * (np.sum(dG1) + tail)

    if evz % 2 != 1:
      H2 = Hijk(np.zeros_like(pperp_limbwd), np.minimum(pperp_limbwd, pperp_limfwd))
      dG2 = dGijk(E_grid[:-1], E_grid[1:], H2[:-1], H2[1:])
      moment2[idx] = 2 * factor_base[idx] * np.sum(dG2)

      H4 = Hijk(pperp_limbwd, pperp_limfwd)
      dG4 = dGijk(E_grid[:-1], E_grid[1:], H4[:-1], H4[1:])
      moment4[idx] = 2 * alpha * factor_base[idx] * np.sum(dG4)

  moment_total = moment1 + moment2 + moment4
  return moment_total, moment1, moment2, moment4

