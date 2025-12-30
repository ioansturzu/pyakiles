"""Translation of ``+akiles2d/+electrons/+parabolic/+semimaxwellian/moment.m``."""

from __future__ import annotations

import warnings
import numpy as np
from scipy.special import gamma, gammainc, gammaincc
from numba import jit, prange
try:
    import numba_scipy
except ImportError:
    pass

from ....simrc import Data

USE_JIT = True

# -----------------------------------------------------------------------------
# JIT IMPLEMENTATION
# -----------------------------------------------------------------------------

@jit(nopython=True, fastmath=True, cache=True)
def _Hijk_jit(a, b, val):
    return max(0.0, gamma(val) * (gammainc(val, b) - gammainc(val, a)))

@jit(nopython=True, fastmath=True, cache=True)
def _dGijk_jit(E_a, E_b, G_a, G_b, val1, val2):
    t1 = gamma(val1) * (G_b * E_a - G_a * E_b) * (gammainc(val1, E_b) - gammainc(val1, E_a))
    t2 = gamma(val2) * (G_a - G_b) * (gammainc(val2, E_b) - gammainc(val2, E_a))
    denom = E_a - E_b
    if abs(denom) < 1e-14:
        return 0.0
    return (t1 + t2) / denom

@jit(nopython=True, fastmath=True, cache=True)
def _prepare_energy_grid_jit(phi_slice, h_slice, r_slice, ip, nintegration, E_grid, pperp_limbwd, pperp_limfwd):
    phi_end = phi_slice[-1]
    E_transition = 1.5 * (phi_slice[ip] - phi_end)
    if np.isinf(phi_end) or E_transition <= 0:
        E_transition = 5.0
        
    n1 = int(nintegration[0])
    n2 = int(nintegration[1])
    sep = E_transition / (n1 - 1)
    f = 1.05
    
    for i in range(n1):
        E_grid[i] = i * E_transition / (n1 - 1)
    for i in range(n2):
        E_grid[n1 + i] = E_transition + sep * (f ** (i + 1) - 1) / (f - 1)

    nE = len(E_grid)
    pperp_limbwd[:] = 0.0
    pperp_limfwd[:] = 0.0
    
    nh = len(h_slice)
    if ip == nh - 1:
        return

    h_ip = h_slice[ip]
    h_ip2 = h_ip * h_ip
    h_ip4 = h_ip2 * h_ip2
    phi_ip = phi_slice[ip]
    r_corr = (r_slice[ip]**2) / h_ip4
    
    for iE in range(nE):
        E = E_grid[iE]
        min_val = np.inf
        
        for k in range(ip + 1):
            h_k = h_slice[k]
            denom = (h_ip2 / (h_k * h_k)) - 1.0
            
            if abs(denom) > 1e-14:
                num = E + phi_slice[k] - phi_ip
                val = num / denom - r_corr
                if not np.isnan(val):
                    if val < min_val:
                        min_val = val
        
        if not np.isnan(min_val) and not np.isinf(min_val):
            pperp_limbwd[iE] = max(0.0, min_val)

        max_val = -np.inf
        valid_fwd = False
        
        for k in range(ip + 1, nh):
            h_k = h_slice[k]
            denom = (h_ip2 / (h_k * h_k)) - 1.0
            
            if abs(denom) > 1e-14:
                num = E + phi_slice[k] - phi_ip
                val = num / denom - r_corr
                if not np.isnan(val):
                    if val > max_val:
                        max_val = val
                        valid_fwd = True
        
        if valid_fwd:
            pperp_limfwd[iE] = max(0.0, max_val)

    if ip == 0:
        pperp_limbwd[:] = np.inf

@jit(nopython=True, parallel=False, fastmath=True, cache=True)
def _run_moment_kernel_jit(ipoints_zero, factor_base, phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha, m1_out, m2_out, m4_out):
    h_val = (2 + evr + evtheta) / 2
    dg1 = (1 + evz) / 2
    dg2 = (3 + evz) / 2
    
    n_points = len(ipoints_zero)
    nE = int(np.sum(nintegrationpoints))
    
    # Pre-allocate workspaces
    E_grid = np.zeros(nE)
    pperp_limbwd = np.zeros(nE)
    pperp_limfwd = np.zeros(nE)
    H1 = np.zeros(nE)
    H2 = np.zeros(nE)
    H4 = np.zeros(nE)
    
    for i in range(n_points):
        ip = ipoints_zero[i]
        factor = factor_base[i]
        
        _prepare_energy_grid_jit(phi, h, r, ip, nintegrationpoints, E_grid, pperp_limbwd, pperp_limfwd)
        
        for k in range(nE):
            H1[k] = _Hijk_jit(pperp_limfwd[k], pperp_limbwd[k], h_val)
            
        sum_dG1 = 0.0
        sum_dG2 = 0.0
        sum_dG4 = 0.0
        
        compute_m2 = (evz % 2 != 1)
        
        for k in range(nE - 1):
             val = _dGijk_jit(E_grid[k], E_grid[k+1], H1[k], H1[k+1], dg1, dg2)
             sum_dG1 += val
             
        tail = H1[-1] * gamma(dg1) * gammaincc(dg1, E_grid[-1])
        m1_out[i] = factor * (sum_dG1 + tail)
        
        if compute_m2:
            for k in range(nE):
                min_lim = min(pperp_limbwd[k], pperp_limfwd[k])
                H2[k] = _Hijk_jit(0.0, min_lim, h_val)
                H4[k] = _Hijk_jit(pperp_limbwd[k], pperp_limfwd[k], h_val)
                
            for k in range(nE - 1):
                sum_dG2 += _dGijk_jit(E_grid[k], E_grid[k+1], H2[k], H2[k+1], dg1, dg2)
                sum_dG4 += _dGijk_jit(E_grid[k], E_grid[k+1], H4[k], H4[k+1], dg1, dg2)

            m2_out[i] = 2 * factor * sum_dG2
            m4_out[i] = 2 * alpha * factor * sum_dG4

# -----------------------------------------------------------------------------
# NUMPY IMPLEMENTATION
# -----------------------------------------------------------------------------

def _Hijk_numpy(a, b, val):
    return np.maximum(0.0, gamma(val) * (gammainc(val, b) - gammainc(val, a)))

def _dGijk_numpy(E_a, E_b, G_a, G_b, val1, val2):
    numerator = gamma(val1) * (G_b * E_a - G_a * E_b) * (gammainc(val1, E_b) - gammainc(val1, E_a))
    numerator += gamma(val2) * (G_a - G_b) * (gammainc(val2, E_b) - gammainc(val2, E_a))
    denom = E_a - E_b
    
    with np.errstate(divide='ignore', invalid='ignore'):
        res = numerator / denom
    res[denom == 0] = 0.0
    return res

def _prepare_energy_grid_numpy(phi_slice, h_slice, r_slice, ip, nintegration):
    nE = int(nintegration.sum())
    E_grid = np.zeros(nE)
    E_transition = 1.5 * (phi_slice[ip] - phi_slice[-1])
    if np.isinf(phi_slice[-1]) or E_transition <= 0:
        E_transition = 5.0
    sep = E_transition / (nintegration[0] - 1)
    f = 1.05
    E_grid[: int(nintegration[0])] = np.linspace(0.0, E_transition, int(nintegration[0]))
    E_grid[int(nintegration[0]) :] = E_transition + sep * (f ** np.arange(1, int(nintegration[1]) + 1) - 1) / (f - 1)

    pperp_limbwd = np.zeros(nE)
    pperp_limfwd = np.zeros(nE)
    if ip == len(phi_slice) - 1:
        return E_grid, pperp_limbwd, pperp_limfwd

    denom = h_slice[ip] ** 2 / h_slice**2 - 1
    with np.errstate(divide="ignore", invalid="ignore"):
        numerator = E_grid[:, None] + phi_slice - phi_slice[ip]
        pperp_vals = numerator / denom

    pperp_vals -= (r_slice[ip] ** 2) / h_slice[ip] ** 4
    backward = pperp_vals[:, : ip + 1]
    forward = pperp_vals[:, ip + 1 :]

    with np.errstate(invalid='ignore'):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', r'All-NaN slice encountered')
            min_bwd = np.nanmin(backward, axis=1)
            max_fwd = np.nanmax(forward, axis=1)

    mask_bwd = ~np.isnan(min_bwd)
    pperp_limbwd[mask_bwd] = np.maximum(0.0, min_bwd[mask_bwd])
    mask_fwd = ~np.isnan(max_fwd)
    pperp_limfwd[mask_fwd] = np.maximum(0.0, max_fwd[mask_fwd])

    if ip == 0:
        pperp_limbwd[:] = np.inf
    return E_grid, pperp_limbwd, pperp_limfwd

def _run_moment_kernel_numpy(ipoints_zero, factor_base, phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha, m1_out, m2_out, m4_out):
    h_val = (2 + evr + evtheta) / 2
    dg1 = (1 + evz) / 2
    dg2 = (3 + evz) / 2
    compute_m2 = (evz % 2 != 1)

    for i, ip in enumerate(ipoints_zero):
        E_grid, pperp_limbwd, pperp_limfwd = _prepare_energy_grid_numpy(phi, h, r, ip, nintegrationpoints)
        factor = factor_base[i]
        
        H1 = _Hijk_numpy(pperp_limfwd, pperp_limbwd, h_val)
        dG1 = _dGijk_numpy(E_grid[:-1], E_grid[1:], H1[:-1], H1[1:], dg1, dg2)
        tail = H1[-1] * gamma(dg1) * gammaincc(dg1, E_grid[-1])
        m1_out[i] = factor * (np.sum(dG1) + tail)

        if compute_m2:
            min_lim = np.minimum(pperp_limbwd, pperp_limfwd)
            H2 = _Hijk_numpy(np.zeros_like(pperp_limbwd), min_lim, h_val)
            dG2 = _dGijk_numpy(E_grid[:-1], E_grid[1:], H2[:-1], H2[1:], dg1, dg2)
            m2_out[i] = 2 * factor * np.sum(dG2)

            H4 = _Hijk_numpy(pperp_limbwd, pperp_limfwd, h_val)
            dG4 = _dGijk_numpy(E_grid[:-1], E_grid[1:], H4[:-1], H4[1:], dg1, dg2)
            m4_out[i] = 2 * alpha * factor * np.sum(dG4)


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
  factor_chunk = factor_base * np.exp(phi[ipoints_zero] - r[ipoints_zero] / h[ipoints_zero] ** 4)

  if USE_JIT:
      _run_moment_kernel_jit(ipoints_zero, factor_chunk, phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha, moment1, moment2, moment4)
  else:
      _run_moment_kernel_numpy(ipoints_zero, factor_chunk, phi, h, r, nintegrationpoints, evz, evr, evtheta, alpha, moment1, moment2, moment4)

  moment_total = moment1 + moment2 + moment4
  return moment_total, moment1, moment2, moment4
