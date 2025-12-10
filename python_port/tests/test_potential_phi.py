import numpy as np

from akiles2d.potential.parabolic import phi


def test_parabolic_phi_basic():
  h = np.array([1.0, 2.0])
  r = np.array([0.0, 1.0])
  phiz = np.array([0.0, -1.0])
  values = phi(h, r, phiz)
  assert values[0] == 0
  assert values[1] < phiz[1]

