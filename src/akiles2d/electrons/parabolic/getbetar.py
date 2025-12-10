"""Translation of ``+akiles2d/+electrons/+parabolic/getbetar.m``."""

from __future__ import annotations

import numpy as np


def getbetar(h: np.ndarray, r: np.ndarray, Jr: np.ndarray | float, ptheta: np.ndarray | float) -> np.ndarray:
  """Compute the radial angle coordinate ``betar``."""

  h_arr = np.asarray(h, dtype=float)
  r_arr = np.asarray(r, dtype=float)
  Jr_arr = np.asarray(Jr, dtype=float)
  ptheta_arr = np.asarray(ptheta, dtype=float)
  numerator = Jr_arr / np.pi + np.abs(ptheta_arr) - np.sqrt(2.0) * r_arr**2 / h_arr**2
  denominator = np.sqrt(Jr_arr / np.pi * (Jr_arr / np.pi + 2 * np.abs(ptheta_arr)))
  ratio = np.divide(numerator, denominator, out=np.zeros_like(numerator, dtype=float), where=denominator != 0)
  betar = np.arccos(ratio) / (2 * np.pi)
  betar = np.where(np.isnan(betar), 0.0, betar)
  return betar

