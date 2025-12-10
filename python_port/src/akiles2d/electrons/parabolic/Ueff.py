"""Translation of ``+akiles2d/+electrons/+parabolic/Ueff.m``."""

from __future__ import annotations

import numpy as np


def Ueff(h: np.ndarray, phiz: np.ndarray | float, Jr: np.ndarray | float, ptheta: np.ndarray | float) -> np.ndarray:
  """Effective potential for axial motion in the parabolic model."""

  h_arr = np.asarray(h, dtype=float)
  phiz_arr = np.asarray(phiz, dtype=float)
  Jr_arr = np.asarray(Jr, dtype=float)
  ptheta_arr = np.asarray(ptheta, dtype=float)
  return -phiz_arr + np.sqrt(2.0) * (Jr_arr / np.pi + np.abs(ptheta_arr)) / h_arr

