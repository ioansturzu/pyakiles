"""
Translation of ``+akiles2d/simrc.m``.

This module defines default configuration structures used by the simulation
and provides a ``simrc`` function to build a fully populated :class:`Data`
instance. The MATLAB code relies heavily on nested structures; here we model
them with typed :mod:`dataclasses` to keep field access explicit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Optional

import numpy as np


@dataclass
class LoggerConfig:
  """Logging configuration mirroring the MATLAB ``logger`` structure."""

  filedebuglevel: int = 3
  screendebuglevel: int = 3
  linelength: int = 80
  logfile: str = ""


@dataclass
class Akiles2DConfig:
  """Top-level AKILES2D settings."""

  simdir: str
  maxiter: int = 200
  tolerance: float = 1e-6
  datafile: str = ""


@dataclass
class PotentialConfig:
  """Potential model selection."""

  model: str = "parabolic"


@dataclass
class IonConfig:
  """Ion model parameters."""

  model: str = "cold"
  chi: float = 0.02
  mu: float = np.inf


@dataclass
class ElectronConfig:
  """Electron model parameters."""

  model: str = "semimaxwellian"
  nintegrationpoints: tuple[int, int] = (500, 300)
  alpha: float = 1.0


@dataclass
class SolverConfig:
  """Root-finding options for the solver stage."""

  phibracket: tuple[float, float] = (-10.0, 0.1)
  errorfcn: str = "netcurrent"
  netcurrent: float = 0.0
  phiinfty: float = -4.0


@dataclass
class PostprocessorConfig:
  """Postprocessing hooks to execute after convergence."""

  postfunctions: list[str] = field(default_factory=lambda: ["moments", "EEDF"])


@dataclass
class Guess:
  """Initial guess for the solution fields."""

  h: np.ndarray
  r: np.ndarray
  phi: np.ndarray
  ne00p: float

  @property
  def npoints(self) -> int:
    """Number of radial grid points in the solution."""

    return int(self.h.size)


@dataclass
class Data:
  """Container for all simulation parameters.

  The MATLAB version uses nested structures. Here we group related settings
  in dedicated dataclasses to simplify downstream typing and validation.
  """

  akiles2d: Akiles2DConfig
  logger: LoggerConfig
  potential: PotentialConfig
  ions: IonConfig
  electrons: ElectronConfig
  solver: SolverConfig
  postprocessor: PostprocessorConfig
  guess: Guess


def _default_guess(npoints: int = 500) -> Guess:
  """Create the default solution guess.

  Args:
    npoints: Number of discrete points in the axial sweep. MATLAB defaults to
      500 with the last point at infinity.

  Returns:
    Guess populated with vectors for ``h``, ``r``, ``phi``, and ``ne00p``.
  """

  h = np.concatenate([np.linspace(1.0, 5.0, npoints - 1), np.array([np.inf])])
  r = np.zeros(npoints)
  phi = np.linspace(0.0, -4.0, npoints)
  ne00p = 0.51
  return Guess(h=h, r=r, phi=phi, ne00p=ne00p)


def simrc(data: Optional[Data | dict[str, object]] = None) -> Data:
  """Create the default configuration structure.

  This mirrors ``+akiles2d/simrc.m``: it prepares nested configuration
  objects, sets the default logging file path, and constructs an initial guess.

  Args:
    data: Optional partially populated configuration to modify. If provided as
      a mapping, keys are merged into the returned dataclass after defaults are
      created.

  Returns:
    Fully populated :class:`Data` instance.
  """

  simdir = str(Path.cwd() / "sims")
  logger = LoggerConfig(logfile=str(Path(simdir) / "log.txt"))
  akiles = Akiles2DConfig(simdir=simdir, datafile=str(Path(simdir) / "data.mat"))
  potential = PotentialConfig()
  ions = IonConfig()
  electrons = ElectronConfig()
  solver = SolverConfig()
  postprocessor = PostprocessorConfig()
  guess = _default_guess()

  defaults = Data(
    akiles2d=akiles,
    logger=logger,
    potential=potential,
    ions=ions,
    electrons=electrons,
    solver=solver,
    postprocessor=postprocessor,
    guess=guess,
  )

  if data is None:
    return defaults

  if isinstance(data, Data):
    return data

  # Merge overrides supplied as a mapping (coarse emulation of MATLAB struct
  # updates). Only known attributes are applied.
  overrides = dict(data)
  for field_name, value in overrides.items():
    if hasattr(defaults, field_name):
      setattr(defaults, field_name, value)  # type: ignore[arg-type]
  return defaults


def apply_user_simrc(defaults: Data, simrc_fn: Callable[[Data], Data]) -> Data:
  """Apply a user-provided ``simrc``-style function.

  MATLAB uses dynamic ``str2func`` calls. Here we expect a Python callable that
  accepts a :class:`Data` and returns a modified copy.
  """

  return simrc_fn(defaults)


def apply_userdata(defaults: Data, userdata: dict[str, object] | None) -> Data:
  """Merge arbitrary ``userdata`` overrides into the configuration."""

  if not userdata:
    return defaults
  for key, value in userdata.items():
    if hasattr(defaults, key):
      setattr(defaults, key, value)  # type: ignore[arg-type]
  return defaults

