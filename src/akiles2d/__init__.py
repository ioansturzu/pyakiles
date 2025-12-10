"""
Python translation of the MATLAB akiles2d package.

This package mirrors the original MATLAB namespace under ``python_port``
while providing typed Python implementations of the simulation routines,
utilities, and postprocessing helpers.
"""

from typing import TYPE_CHECKING, Tuple

from .simrc import simrc, Akiles2DConfig, LoggerConfig, PotentialConfig, IonConfig, ElectronConfig, SolverConfig, PostprocessorConfig, Guess, Data
from .preprocessor import preprocessor

if TYPE_CHECKING:  # pragma: no cover - used for type checkers only
  from .akiles2d import akiles2d as _akiles2d


def akiles2d(simrcfile: str | None = None, userdata: dict[str, object] | None = None) -> Tuple[Data, dict[str, object]]:
  """Entry point for running the Akiles2D simulation.

  A thin wrapper that performs a lazy import to avoid eagerly loading
  :mod:`akiles2d.akiles2d` when the package itself is imported. This prevents
  Python's module runner from issuing duplicate import warnings when executed
  via ``python -m akiles2d.akiles2d``.
  """

  from .akiles2d import akiles2d as _akiles2d

  return _akiles2d(simrcfile, userdata)

__all__ = [
  "simrc",
  "Akiles2DConfig",
  "LoggerConfig",
  "PotentialConfig",
  "IonConfig",
  "ElectronConfig",
  "SolverConfig",
  "PostprocessorConfig",
  "Guess",
  "Data",
  "preprocessor",
  "akiles2d",
]

