"""Translation of ``+akiles2d/+electrons/+parabolic/getmomenta.m``."""

from __future__ import annotations

import numpy as np


def getmomenta(h: np.ndarray, r: np.ndarray, phiz: np.ndarray, vz: np.ndarray, vr: np.ndarray, vtheta: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
  """Recover energy and momenta from velocity components."""

  h_arr = np.asarray(h, dtype=float)
  r_arr = np.asarray(r, dtype=float)
  phiz_arr = np.asarray(phiz, dtype=float)
  vz_arr = np.asarray(vz, dtype=float)
  vr_arr = np.asarray(vr, dtype=float)
  vtheta_arr = np.asarray(vtheta, dtype=float)

  ptheta = np.abs(r_arr * vtheta_arr)
  E = (vz_arr**2 + vr_arr**2 + vtheta_arr**2) / 2.0 - phiz_arr + r_arr**2 / h_arr**4
  Jr = (np.sqrt(0.5) * (E + phiz_arr - vz_arr**2 / 2.0) * h_arr**2 - np.abs(ptheta)) * np.pi
  return E, Jr, ptheta

