"""
Reproduction of Figure 1 (estimated) from *Kinetic electron model for plasma
thruster plumes* (2018): axial potential and density profiles.

The original article plots the on-axis electrostatic potential and the electron
and ion densities. This example runs the AKILES2D solver with a trimmed grid and
integration settings for quick turnaround, then overlays potential and density
profiles versus the normalized position ``h``. Density magnitudes are computed
from the kinetic moments produced by the repository's post-processing tools.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure the local source tree is importable when executed from the repo root.
sys.path.append("src")

from akiles2d.akiles2d import akiles2d
from akiles2d.simrc import (
  Akiles2DConfig,
  ElectronConfig,
  Guess,
  PostprocessorConfig,
)


def run_simulation() -> tuple[dict, dict]:
  """Run a fast AKILES2D solve tailored for plotting profiles.

  The configuration mirrors the article but uses fewer grid points and energy
  integration bins to keep the example interactive.
  """

  npoints = 80
  h = np.concatenate([np.linspace(1.0, 4.0, npoints - 1), np.array([np.inf])])
  r = np.zeros(npoints)
  phi_guess = np.linspace(0.0, -3.0, npoints)

  guess = Guess(h=h, r=r, phi=phi_guess, ne00p=0.5)
  simdir = Path("examples/python/sims_fig01")
  userdata = {
    "guess": guess,
    "electrons": ElectronConfig(nintegrationpoints=(80, 40), alpha=1.0),
    "akiles2d": Akiles2DConfig(
      simdir=str(simdir),
      maxiter=3,
      tolerance=1e-3,
      datafile=str(simdir / "data.mat"),
    ),
    "postprocessor": PostprocessorConfig(postfunctions=["moments", "EEDF"]),
  }

  data, solution = akiles2d(userdata=userdata)
  return data, solution


def plot_profiles(solution: dict) -> None:
  h = np.asarray(solution["h"], dtype=float)
  phi = np.asarray(solution["phi"], dtype=float)
  ne = np.asarray(solution["electrons"]["n"], dtype=float)
  ni = np.asarray(solution["ions"]["n"], dtype=float)

  fig, ax1 = plt.subplots(figsize=(6, 4))
  ax1.plot(h, phi, label=r"$\phi$ (V)", color="tab:blue")
  ax1.set_xlabel("Normalized position h")
  ax1.set_ylabel("Potential (V)", color="tab:blue")
  ax1.tick_params(axis="y", labelcolor="tab:blue")

  ax2 = ax1.twinx()
  ax2.plot(h, ne, label=r"$n_e$", color="tab:red", linestyle="--")
  ax2.plot(h, ni, label=r"$n_i$", color="tab:green", linestyle=":")
  ax2.set_ylabel("Density (normalized)")

  lines, labels = ax1.get_legend_handles_labels()
  lines2, labels2 = ax2.get_legend_handles_labels()
  ax2.legend(lines + lines2, labels + labels2, loc="upper right")
  ax1.set_title("Figure 1: Potential and density along plume axis")
  fig.tight_layout()
  fig.savefig(Path(__file__).with_suffix(".png"))
  plt.show()


def main() -> None:
  _, solution = run_simulation()
  plot_profiles(solution)

  # Save results for CI comparison
  import json
  
  results = {
      "h": np.asarray(solution["h"], dtype=float).tolist(),
      "phi": np.asarray(solution["phi"], dtype=float).tolist(),
      "ne": np.asarray(solution["electrons"]["n"], dtype=float).tolist(),
      "ni": np.asarray(solution["ions"]["n"], dtype=float).tolist(),
  }
  
  # Handle infinity for JSON compliance if necessary, though standard json might error on inf.
  # Let's replace inf with a large number or string for safety, or just let users handle it.
  # For this specific case, h[-1] is inf.
  if len(results["h"]) > 0 and np.isinf(results["h"][-1]):
      results["h"][-1] = "inf"

  with open(Path("examples/python/fig01_results.json"), "w") as f:
      json.dump(results, f, indent=2)

if __name__ == "__main__":
  main()
