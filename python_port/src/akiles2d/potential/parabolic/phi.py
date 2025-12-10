"""Translation of ``+akiles2d/+potential/+parabolic/phi.m``."""

from __future__ import annotations

import numpy as np


def phi(h: np.ndarray, r: np.ndarray, phiz: np.ndarray | float) -> np.ndarray:
  """Compute the parabolic potential at radius ``r``."""

  return -np.asarray(r, dtype=float) ** 2 / np.asarray(h, dtype=float) ** 4 + np.asarray(phiz, dtype=float)

