import numpy as np

from akiles2d.electrons.parabolic import Ueff, getbetar, getmomenta, getr, getvelocities


def test_ueff_and_velocities():
  U = Ueff(2.0, -0.5, 0.2, 0.1)
  assert U > 0
  vz, vr, vtheta = getvelocities(2.0, 1.0, -0.5, 1.0, 0.2, 0.1)
  assert vz > 0
  assert vtheta >= 0


def test_betar_round_trip():
  h = np.array([1.0, 2.0])
  betar = np.array([0.0, 0.25])
  Jr = np.array([0.1, 0.2])
  ptheta = np.array([0.0, 0.05])
  r = getr(h, betar, Jr, ptheta)
  recovered = getbetar(h, r, Jr, ptheta)
  assert np.allclose(recovered, betar)


def test_getmomenta_shapes():
  h = np.array([1.0, 1.5])
  r = np.array([0.0, 0.2])
  phiz = np.array([0.0, -0.2])
  vz = np.array([0.5, 0.7])
  vr = np.array([0.1, 0.2])
  vtheta = np.array([0.0, 0.05])
  E, Jr, ptheta = getmomenta(h, r, phiz, vz, vr, vtheta)
  assert E.shape == h.shape
  assert Jr[1] > 0
  assert ptheta[0] == 0

