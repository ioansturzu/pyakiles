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

  # Vectorized calculation
  # Shapes: E_grid (nE, 1), phi_slice (1, nh) -> broadcasting (nE, nh)
  denom = h_slice[ip] ** 2 / h_slice**2 - 1
  
  with np.errstate(divide="ignore", invalid="ignore"):
    # (nE, 1) + (nh,) - scalar -> (nE, nh)
    numerator = E_grid[:, None] + phi_slice - phi_slice[ip]
    # Division by (nh,) broadcasts correctly
    pperp_vals = np.divide(numerator, denom, where=denom != 0)
    # Fill masked values with NaN (np.divide leaves uninitialized or 0 where mask is False usually, 
    # but strictly we want NaN for the min/max logic to work)
    # Actually np.divide with 'where' retains original values in 'out' if provided, 
    # or 0 if not initialized. It's safer to initialize or handle masks.
    # Let's use direct division and let numpy handle infs/nans, then correct.
    pperp_vals = numerator / denom # This generates infs/nans which is fine.

  # Apply correction term
  pperp_vals -= (r_slice[ip] ** 2) / h_slice[ip] ** 4
  
  # Filter invalid values: only replace NaNs, preserve Infs!
  # np.isnan is false for Inf.
  # So we just leave it alone. The previous code cleared Infs which was WRONG.
  # pperp_vals[~np.isfinite(pperp_vals)] = np.nan  <-- REMOVED

  # Split into backward and forward regions
  # backward: indices 0 to ip (inclusive)
  # forward: indices ip+1 to end
  backward = pperp_vals[:, : ip + 1]
  forward = pperp_vals[:, ip + 1 :]

  # Compute limits using vectorized min/max along axis 1 (spatial dimension)
  # All warnings for empty slice or all-NaN slice are expected and safe (result is NaN)
  with np.errstate(invalid='ignore'):
      min_bwd = np.nanmin(backward, axis=1)
      max_fwd = np.nanmax(forward, axis=1)

  # Where valid, take max(0, val). Where NaN, keep 0 (initialized).
  # np.maximum handles NaNs by propagating them or ignoring? 
  # np.maximum(0, nan) -> nan.
  # We want 0 if NaN? Or Inf?
  # If min_bwd is Inf, result Inf.
  # If min_bwd is NaN, result NaN?
  # MATLAB Pperp_limbwd initialized to 0.
  # If nanmin returns NaN, we want to keep it?
  # No, moment calculation `Hijk` handles limits.
  # If limit is 0, Hijk uses 0.
  # So we need to handle NaNs.
  
  mask_bwd = np.isfinite(min_bwd) | np.isinf(min_bwd) # True for finite and inf, False for NaN
  # Actually isfinite is False for Inf.
  # We want to ACT on valid values (including Inf).
  # So mask should be ~np.isnan(min_bwd).
  
  mask_bwd = ~np.isnan(min_bwd)
  pperp_limbwd[mask_bwd] = np.maximum(0.0, min_bwd[mask_bwd])
  
  mask_fwd = ~np.isnan(max_fwd)
  pperp_limfwd[mask_fwd] = np.maximum(0.0, max_fwd[mask_fwd])

  if ip == 0:
    pperp_limbwd[0] = np.inf
  return E_grid, pperp_limbwd, pperp_limfwd


from concurrent.futures import ThreadPoolExecutor

def _Hijk(a, b, val):
    return np.maximum(0.0, gamma(val) * (gammainc(val, b) - gammainc(val, a)))

def _dGijk(E_a, E_b, G_a, G_b, val1, val2):
    numerator = gamma(val1) * (G_b * E_a - G_a * E_b) * (gammainc(val1, E_b) - gammainc(val1, E_a))
    numerator += gamma(val2) * (G_a - G_b) * (gammainc(val2, E_b) - gammainc(val2, E_a))
    denom = E_a - E_b
    return numerator / denom

def _compute_point_moment(args):
    ip, factor, phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha = args
    
    # Pre-calculate constants for Hijk/dGijk to avoid repeated gamma calls if costly (optional optimization)
    # Passed as args to helpers
    h_val = (2 + evr + evtheta) / 2
    dg1 = (1 + evz) / 2
    dg2 = (3 + evz) / 2
    
    E_grid, pperp_limbwd, pperp_limfwd = _prepare_energy_grid(phi, h, r, ip, nintegrationpoints)
    
    H1 = _Hijk(pperp_limfwd, pperp_limbwd, h_val)
    dG1 = _dGijk(E_grid[:-1], E_grid[1:], H1[:-1], H1[1:], dg1, dg2)
    tail = H1[-1] * gamma(dg1) * gammaincc(dg1, E_grid[-1])
    m1 = factor * (np.sum(dG1) + tail)

    m2 = 0.0
    m4 = 0.0
    
    if evz % 2 != 1:
      H2 = _Hijk(np.zeros_like(pperp_limbwd), np.minimum(pperp_limbwd, pperp_limfwd), h_val)
      dG2 = _dGijk(E_grid[:-1], E_grid[1:], H2[:-1], H2[1:], dg1, dg2)
      m2 = 2 * factor * np.sum(dG2)

      H4 = _Hijk(pperp_limbwd, pperp_limfwd, h_val)
      dG4 = _dGijk(E_grid[:-1], E_grid[1:], H4[:-1], H4[1:], dg1, dg2)
      m4 = 2 * alpha * factor * np.sum(dG4)
      
    return m1, m2, m4

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
  
  moment1 = np.zeros(nipoints)
  moment2 = np.zeros(nipoints)
  moment4 = np.zeros(nipoints)
  moment_total = np.zeros(nipoints)

  if evr % 2 == 1 or evtheta % 2 == 1:
    return moment_total, moment1, moment2, moment4

  factor_base = ne00p * 2 ** ((evz + evr + evtheta) / 2) * gamma((1 + evr) / 2) * gamma((1 + evtheta) / 2) / gamma(1 + (evr + evtheta) / 2) / np.pi ** 1.5
  factor_base *= np.exp(phi[ipoints_zero] - r[ipoints_zero] / h[ipoints_zero] ** 4)

  # Prepare arguments for parallel execution
  # (ip, factor, phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha)
  work_args = []
  for idx, ip in enumerate(ipoints_zero):
      work_args.append((ip, factor_base[idx], phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha))

  # Use ThreadPoolExecutor
  USE_PARALLEL = False
  
  if USE_PARALLEL:
      with ThreadPoolExecutor() as executor:
          results = list(executor.map(_compute_point_moment, work_args))
  else:
      results = [_compute_point_moment(arg) for arg in work_args]
      
  # Unpack results
  for idx, (m1, m2, m4) in enumerate(results):
      moment1[idx] = m1
      moment2[idx] = m2
      moment4[idx] = m4

  moment_total = moment1 + moment2 + moment4
  return moment_total, moment1, moment2, moment4

