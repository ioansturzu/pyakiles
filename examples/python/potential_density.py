"""
Axial potential and density profiles (inspired by *Kinetic electron model for plasma thruster plumes*).

This example runs the AKILES2D solver with a trimmed grid and integration settings for quick turnaround,
then overlays potential and density profiles versus the normalized position ``h``. Density magnitudes
are computed from the kinetic moments produced by the repository's post-processing tools.
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


from akiles2d.simrc import Akiles2DConfig, simrc

def run_simulation() -> tuple[dict, dict]:
  """Run the standard AKILES2D solve (default parameters)."""
  simdir = Path("examples/python/sims_potential_density")
  
  # Override settings using dataclass to preserve object structure
  userdata = {
    "akiles2d": Akiles2DConfig(simdir=str(simdir), datafile=str(simdir / "data.mat"))
  }
  
  # Run simulation using defaults (implicit) + userdata overrides
  data, solution = akiles2d(userdata=userdata)
  return data, solution


def plot_profiles(solution: dict) -> None:
  h = np.asarray(solution["h"], dtype=float)
  phi = np.asarray(solution["phi"], dtype=float)
  ne = np.asarray(solution["electrons"]["n"], dtype=float)
  ni = np.asarray(solution["ions"]["n"], dtype=float)
  
  print(f"DEBUG: Final ne00p: {solution.get('ne00p')}")
  print(f"DEBUG: ni[0] (at h=1): {ni[0]}")
  print(f"DEBUG: ne[0] (at h=1): {ne[0]}")
  print(f"DEBUG: phi[0]: {phi[0]}")

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
  ax1.set_title("Potential and density along plume axis")
  fig.tight_layout()
  fig.savefig(Path(__file__).with_suffix(".png"))
  # plt.show() # Disabled for CI/headless


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
  
  if len(results["h"]) > 0 and np.isinf(results["h"][-1]):
      results["h"][-1] = "inf"

  with open(Path(__file__).with_name("potential_density_results.json"), "w") as f:
      json.dump(results, f, indent=2)

if __name__ == "__main__":
  main()
