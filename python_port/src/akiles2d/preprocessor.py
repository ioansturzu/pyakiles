"""
Translation of ``+akiles2d/+preprocessor/preprocessor.m``.

The preprocessor builds a full :class:`~akiles2d.simrc.Data` instance by
layering default values from :func:`akiles2d.simrc.simrc`, optional overrides
from a user-provided ``simrc`` callable, and arbitrary ``userdata`` mappings.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Callable, Optional

from .simrc import Data, apply_user_simrc, apply_userdata, simrc


def _load_simrc_callable(simrcfile: str) -> Callable[[Data], Data]:
  """Load a Python callable representing a MATLAB-style ``simrc`` function."""

  module_path = Path(simrcfile)
  module_name = module_path.stem
  if module_path.parent != Path("."):
    import sys

    sys.path.insert(0, str(module_path.parent.resolve()))
  module: ModuleType = import_module(module_name)
  if not hasattr(module, "simrc"):
    raise AttributeError(f"Module {module_name} does not define simrc")
  func = getattr(module, "simrc")
  if not callable(func):
    raise TypeError("simrc attribute must be callable")
  return func


def preprocessor(simrcfile: Optional[str] = None, userdata: Optional[dict[str, object]] = None) -> Data:
  """Prepare the simulation configuration structure.

  Args:
    simrcfile: Optional path to a Python module containing a ``simrc``
      function. This mirrors MATLAB's ability to load user ``simrc`` files.
    userdata: Arbitrary mapping of overrides applied after the user ``simrc``
      function.

  Returns:
    Fully populated :class:`Data` ready for simulation.
  """

  data = simrc()

  if simrcfile:
    func = _load_simrc_callable(simrcfile)
    data = apply_user_simrc(data, func)

  data = apply_userdata(data, userdata)

  data.akiles2d.datafile = str(Path(data.akiles2d.simdir) / "data.mat")
  data.logger.logfile = str(Path(data.akiles2d.simdir) / "log.txt")
  return data

