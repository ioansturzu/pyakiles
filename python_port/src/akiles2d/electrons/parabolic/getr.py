"""Translation of ``+akiles2d/+electrons/+parabolic/getr.m``."""

from __future__ import annotations

import numpy as np


def getr(h: np.ndarray, betar: np.ndarray, Jr: np.ndarray | float, ptheta: np.ndarray | float) -> np.ndarray:
  """Invert :func:`getbetar` to recover ``r``."""

  h_arr = np.asarray(h, dtype=float)
  betar_arr = np.asarray(betar, dtype=float)
  Jr_arr = np.asarray(Jr, dtype=float)
  ptheta_arr = np.asarray(ptheta, dtype=float)
  return np.sqrt((h_arr**2 / np.sqrt(2.0)) * (Jr_arr / np.pi + np.abs(ptheta_arr) - np.cos(2 * np.pi * betar_arr) * np.sqrt(Jr_arr / np.pi * (Jr_arr / np.pi + 2 * np.abs(ptheta_arr)))))

