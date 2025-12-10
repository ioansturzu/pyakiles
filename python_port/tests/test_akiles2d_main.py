import numpy as np

from akiles2d.akiles2d import akiles2d
from akiles2d.simrc import simrc


def test_main_single_iteration(tmp_path):
  userdata = {
    "akiles2d": simrc().akiles2d,
    "guess": simrc().guess,
  }
  userdata["akiles2d"].simdir = str(tmp_path)
  userdata["akiles2d"].maxiter = 0
  userdata["guess"].h = np.array([1.0, 2.0])
  userdata["guess"].r = np.array([0.0, 0.0])
  userdata["guess"].phi = np.array([0.0, -0.1])
  userdata["guess"].ne00p = 0.2
  data, solution = akiles2d(userdata=userdata)
  assert solution["npoints"] == 2
  assert tmp_path.exists()

