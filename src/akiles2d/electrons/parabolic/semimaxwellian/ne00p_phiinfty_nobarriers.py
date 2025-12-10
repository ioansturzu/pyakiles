"""Translation of ``ne00p_phiinfty_nobarriers.m``."""

from __future__ import annotations

from typing import Tuple

from scipy.optimize import root_scalar
from scipy.special import erf
import numpy as np


def ne00p_phiinfty_nobarriers(chi: float) -> Tuple[float, float]:
  """Compute ``ne00p`` and ``phiinfty`` assuming no intermediate barriers."""

  eq1 = lambda phiinfty: 1 + erf(np.sqrt(-phiinfty)) - np.sqrt(-2 * phiinfty / np.pi) * np.exp(phiinfty)
  eq2 = lambda phiinfty: np.sqrt(2 / np.pi) * (1 - phiinfty) * np.exp(phiinfty) / chi

  root = root_scalar(lambda val: eq1(val) - eq2(val), bracket=(-10.0, 0.0), x0=-5.0)
  phiinfty = float(root.root)
  ne00p = 1 / eq2(phiinfty)
  return float(ne00p), phiinfty

