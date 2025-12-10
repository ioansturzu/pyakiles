"""Translation of ``+akiles2d/+electrons/+parabolic/getvelocities.m``."""

from __future__ import annotations

import numpy as np


def getvelocities(h: np.ndarray, r: np.ndarray, phiz: np.ndarray | float, E: np.ndarray | float, Jr: np.ndarray | float, ptheta: np.ndarray | float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
  """Compute absolute velocity components for given invariants."""

  h_arr = np.asarray(h, dtype=float)
  r_arr = np.asarray(r, dtype=float)
  phiz_arr = np.asarray(phiz, dtype=float)
  E_arr = np.asarray(E, dtype=float)
  Jr_arr = np.asarray(Jr, dtype=float)
  ptheta_arr = np.asarray(ptheta, dtype=float)

  temp = np.sqrt(2.0) * (Jr_arr / np.pi + np.abs(ptheta_arr)) / h_arr**2
  absvz = np.sqrt(np.maximum(0.0, (E_arr + phiz_arr - temp) * 2.0))
  absvtheta = np.abs(np.divide(ptheta_arr, r_arr, out=np.zeros_like(ptheta_arr, dtype=float), where=r_arr != 0))
  absvr = np.sqrt(np.maximum(0.0, (temp - (r_arr**2) / h_arr**4) * 2.0 - absvtheta**2))
  return absvz, absvr, absvtheta

