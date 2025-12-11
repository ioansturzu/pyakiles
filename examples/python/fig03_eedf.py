"""EEDF example using the AKILES2D postprocessor.

This script demonstrates how to extract and plot electron energy distribution
functions (EEDFs) at representative locations along the plume. It uses the same
fast simulation settings as the other Python examples but does **not** attempt
an exact reproduction of any specific figure from the reference paper.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append("src")

from akiles2d.akiles2d import akiles2d
from akiles2d.simrc import Akiles2DConfig, ElectronConfig, Guess, PostprocessorConfig


def run_simulation() -> dict:
  npoints = 80
  h = np.concatenate([np.linspace(1.0, 4.0, npoints - 1), np.array([np.inf])])
  r = np.zeros(npoints)
  phi_guess = np.linspace(0.0, -3.0, npoints)
  guess = Guess(h=h, r=r, phi=phi_guess, ne00p=0.5)
  simdir = Path("examples/python/sims_fig03")
  simdir.mkdir(parents=True, exist_ok=True)
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
  ax.set_title("EEDF along plume axis (example)")
  ax.legend()
  fig.tight_layout()
  fig.savefig(Path(__file__).with_suffix(".png"))
  plt.show()


def main() -> None:
  solution = run_simulation()
  plot_eedf(solution)


if __name__ == "__main__":
  main()
