from pathlib import Path

from akiles2d.preprocessor import preprocessor
from akiles2d.simrc import simrc


def test_preprocessor_override_logfile(tmp_path: Path):
  userdata = {"akiles2d": simrc().akiles2d}
  userdata["akiles2d"].simdir = str(tmp_path)
  data = preprocessor(None, userdata)
  assert str(tmp_path) in data.logger.logfile

