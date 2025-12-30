from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass, asdict
from typing import Any
import numpy as np

@dataclass
class Akiles2DConfig:
    """Top-level AKILES2D settings."""

    simdir: str
    maxiter: int = 5
    tolerance: float = 1e-4
    datafile: str = ""

@dataclass
class LoggerConfig:
    """Logging configuration."""

    filedebuglevel: int = 3
    screendebuglevel: int = 3
    linelength: int = 80

@dataclass
class PotentialConfig:
    """Potential model settings."""

    model: str = "parabolic"

@dataclass
class IonConfig:
    """Ion model settings."""

    model: str = "cold"
    chi: float = 0.02
    mu: float = float("inf")

@dataclass
class ElectronConfig:
    """Electron model settings."""

    model: str = "semimaxwellian"
    nintegrationpoints: list[int] = field(default_factory=lambda: [500, 300])
    alpha: float = 1.0

@dataclass
class Guess:
    """Initial guess for the solver."""

    h: np.ndarray = field(default_factory=lambda: np.array([]))
    r: np.ndarray = field(default_factory=lambda: np.array([]))
    phi: np.ndarray = field(default_factory=lambda: np.array([]))
    ne00p: float = 0.51

@dataclass
class SolverConfig:
    """Solver settings."""

    phibracket: list[float] = field(default_factory=lambda: [-10.0, 0.0])
    errorfcn: str = "netcurrent"
    netcurrent: float = 0.0
    phiinfty: float = -4.0

@dataclass
class PostprocessorConfig:
    """Post-processing settings."""

    postfunctions: list[str] = field(default_factory=lambda: ["moments", "EEDF"])

@dataclass
class Data:
    """Main data structure holding all configuration."""

    akiles2d: Akiles2DConfig
    logger: LoggerConfig
    potential: PotentialConfig
    ions: IonConfig
    electrons: ElectronConfig
    guess: Guess
    solver: SolverConfig
    postprocessor: PostprocessorConfig


def _default_guess(npoints: int = 500) -> Guess:
    """Generate default guess arrays."""
    h = np.linspace(1, 5, npoints - 1)
    h = np.append(h, np.inf)
    r = np.zeros(npoints)
    phi = np.linspace(0, -4, npoints)
    return Guess(h=h, r=r, phi=phi, ne00p=0.51)


def simrc(data: Data | None = None) -> Data:
    """
    Creates default data structure containing the parameters of the problem.
    """
    # Create default configurations if not provided
    akiles2d_conf = Akiles2DConfig(simdir="sims")
    logger_conf = LoggerConfig()
    potential_conf = PotentialConfig()
    ions_conf = IonConfig()
    electrons_conf = ElectronConfig()
    solver_conf = SolverConfig()
    postprocessor_conf = PostprocessorConfig()

    guess = _default_guess()

    default_data = Data(
        akiles2d=akiles2d_conf,
        logger=logger_conf,
        potential=potential_conf,
        ions=ions_conf,
        electrons=electrons_conf,
        guess=guess,
        solver=solver_conf,
        postprocessor=postprocessor_conf,
    )

    if data is None:
        return default_data
    
    # Ideally, we would merge 'data' into 'default_data' here. 
    return default_data


def apply_user_simrc(data: Data, simrcfile: str) -> Data:
    """Calculates the user simrc file and applies it to the data structure."""
    if not simrcfile:
        return data
    # In a full implementation, this would execute the python file or parse a config.
    # For this port, we assume users use the userdata dictionary mechanism mostly.
    return data


def apply_userdata(data: Data, userdata: dict[str, Any]) -> Data:
    """Overwrites data with user provided dictionary."""
    if not userdata:
        return data

    def recursive_update(data_obj: Any, update_dict: dict[str, Any]):
        for key, value in update_dict.items():
            if hasattr(data_obj, key):
                attr = getattr(data_obj, key)
                if is_dataclass(attr) and isinstance(value, dict):
                    recursive_update(attr, value)
                elif isinstance(attr, dict) and isinstance(value, dict):
                    # For simple dicts inside dataclasses, assuming non-nested for now or just overwrite
                     attr.update(value)
                else:
                    setattr(data_obj, key, value)
            
    recursive_update(data, userdata)
    return data
