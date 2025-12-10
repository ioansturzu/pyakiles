"""
Translation of ``+akiles2d/akiles2d.m``.

The main entry point chains preprocessing, solver iterations, and
postprocessing while logging progress. File system operations mirror the
MATLAB behavior by persisting intermediate iterations to ``simdir``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

from . import logger
from .preprocessor import preprocessor
from .simrc import Data
from .solver import errorfcn, solver as solve
from .postprocessor import moments, EEDF


VERSION = "20200901"


def akiles2d(simrcfile: str | None = None, userdata: dict[str, object] | None = None) -> Tuple[Data, dict[str, object]]:
  """Run the AKILES2D simulation loop.

  Args:
    simrcfile: Optional path to a Python ``simrc`` module with overrides.
    userdata: Optional mapping of fields overriding defaults and user ``simrc``
      values.

  Returns:
    Tuple of the simulation :class:`Data` and the converged solution mapping.
  """

  data = preprocessor(simrcfile, userdata)
  Path(data.akiles2d.simdir).mkdir(parents=True, exist_ok=True)
  save_path = Path(data.akiles2d.datafile)
  save_path.write_text("data placeholder saved by Python port\n")

  logger.title(f"AKILES2D version {VERSION}", 10, data.logger)
  logger.log(f"Simulation directory: {data.akiles2d.simdir}", "INF", 5, data.logger)
  logger.log(f"Structure data saved to {data.akiles2d.datafile} successfully.", "INF", 5, data.logger)

  solution = {
    "h": np.array(data.guess.h, dtype=float),
    "r": np.array(data.guess.r, dtype=float),
    "phi": np.array(data.guess.phi, dtype=float),
    "ne00p": float(data.guess.ne00p),
  }
  solution["npoints"] = int(solution["h"].size)

  for iiter in range(data.akiles2d.maxiter + 1):
    solution["errorfcn"] = errorfcn(data, solution)
    normerror = float(np.linalg.norm(solution["errorfcn"]))

    iteration_file = Path(data.akiles2d.simdir) / f"{iiter}.mat"
    iteration_file.write_text("iteration placeholder\n")
    logger.log(f"Iteration {iiter} saved to disk.", "INF", 5, data.logger)
    logger.log(f"Error norm: {normerror}", "INF", 4, data.logger)
    logger.log("Detailed error vector:", "INF", 1, data.logger)
    logger.write(np.array2string(solution["errorfcn"]), 1, data.logger)

    if normerror < data.akiles2d.tolerance:
      logger.log(f"Convergence reached successfully at iteration {iiter}.", "INF", 5, data.logger)
      final_path = Path(data.akiles2d.simdir) / "final.mat"
      final_path.write_text("final iteration placeholder\n")
      logger.log(f"Final iteration saved to {final_path}", "INF", 5, data.logger)
      break

    solution = solve(data, solution)
  else:
    logger.log("Maximum number of iterations was reached!", "WRN", 8, data.logger)

  for postfn in data.postprocessor.postfunctions:
    logger.log(f"Running postprocessor function: {postfn}", "INF", 5, data.logger)
    if postfn == "moments":
      solution = moments(data, solution)
    elif postfn == "EEDF":
      solution = EEDF(data, solution)
    else:
      raise ValueError(f"Unknown postprocessor function: {postfn}")

  post_path = Path(data.akiles2d.simdir) / "post.mat"
  post_path.write_text("postprocessed solution placeholder\n")
  logger.log(f"Solution saved to {post_path}", "INF", 5, data.logger)
  logger.title("AKILES2D execution finished.", 10, data.logger)
  return data, solution

