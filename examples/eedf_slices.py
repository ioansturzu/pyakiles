"""
Electron energy distribution functions (EEDF) at selected axial positions (inspired by *Kinetic electron model for plasma thruster plumes*).

The repository's EEDF postprocessor returns the partial contributions of the
three electron populations. This example plots the total EEDF versus energy for
upstream, mid-plume, and far-plume locations using the same fast simulation
setup as other examples.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append("src")

from akiles2d.akiles2d import akiles2d
from akiles2d.simrc import Akiles2DConfig, ElectronConfig, Guess, PostprocessorConfig


from akiles2d.simrc import Akiles2DConfig

def run_simulation() -> dict:
  """Run the standard AKILES2D solve (default parameters)."""
  simdir = Path("examples/sims_eedf_slices")
  
  userdata = {
    "akiles2d": Akiles2DConfig(simdir=str(simdir), datafile=str(simdir / "data.mat"))
  }
  
  _, solution = akiles2d(userdata=userdata)
  return solution


def plot_eedf(solution: dict) -> None:
  h = np.asarray(solution["h"], dtype=float)
  Ek = np.asarray(solution["electrons"]["Ek"], dtype=float)
  eedf = np.asarray(solution["electrons"]["EEDF"], dtype=float)
  indices = [0, len(h) // 2, len(h) - 2]
  labels = ["Injection", "Mid plume", "Far plume"]

  fig, ax = plt.subplots(figsize=(6.5, 4))
  for idx, label in zip(indices, labels):
    ax.plot(Ek[idx], eedf[idx], label=f"{label} (h={h[idx]:.2f})")

  ax.set_xlabel("Electron energy E (normalized)")
  ax.set_ylabel("EEDF (a.u.)")
  ax.set_yscale("log")
  ax.set_xlim(0, 20) # Limit x-axis to relevant energy range
  ax.set_ylim(1e-13, 1e2) # Limit y-axis to match reference
  ax.set_title("Electron energy distribution along plume")
  ax.legend()
  fig.tight_layout()
  fig.savefig(Path(__file__).with_suffix(".png"))
  plt.show()


def main() -> None:
  solution = run_simulation()
  plot_eedf(solution)

  # Save results for CI comparison
  import json

  h = np.asarray(solution["h"], dtype=float)
  Ek = np.asarray(solution["electrons"]["Ek"], dtype=float)
  eedf = np.asarray(solution["electrons"]["EEDF"], dtype=float)
  
  # Export full arrays or selected slices? Let's export the slices used in the plot for simplicity,
  # or better yet, the full EEDF at those indices so we can verify exact numbers.
  indices = [0, len(h) // 2, len(h) - 2]
  
  results = {
      "h_indices": indices,
      "h_values": h[indices].tolist(),
      "Ek": [Ek[i].tolist() for i in indices],
      "EEDF": [eedf[i].tolist() for i in indices]
  }

  with open(Path(__file__).with_name("eedf_slices_results.json"), "w") as f:
      json.dump(results, f, indent=2)


if __name__ == "__main__":
  main()
