"""
Approximate reproduction of Figure 2 from *Kinetic electron model for plasma
thruster plumes* (2018): parallel/perpendicular temperatures and axial heat
flux derived from kinetic moments.

The AKILES2D postprocessor returns the necessary electron moments. This script
reuses the fast configuration from Figure 1 to extract temperatures and heat
flux along the normalized axial coordinate ``h``.
"""

import sys
from pathlib import Path

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
  simdir = Path("examples/python/sims_fig02")
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


def plot_thermodynamics(solution: dict) -> None:
  h = np.asarray(solution["h"], dtype=float)
  Te_par = np.asarray(solution["electrons"]["Tz"], dtype=float)
  Te_perp = np.asarray(solution["electrons"]["Tr"], dtype=float)
  qz = np.asarray(solution["electrons"]["qzz"], dtype=float)

  fig, ax = plt.subplots(figsize=(6, 4))
  ax.plot(h, Te_par, label=r"$T_{\parallel}$", color="tab:orange")
  ax.plot(h, Te_perp, label=r"$T_{\perp}$", color="tab:purple", linestyle="--")
  ax.set_xlabel("Normalized position h")
  ax.set_ylabel("Temperature (normalized)")
  ax.legend(loc="upper right")
  ax.set_title("Figure 2: Electron temperatures")
  fig.tight_layout()
  fig.savefig(Path(__file__).with_suffix("_temps.png"))

  fig2, ax2 = plt.subplots(figsize=(6, 3.5))
  ax2.plot(h, qz, label=r"$q_{z}$", color="tab:brown")
  ax2.set_xlabel("Normalized position h")
  ax2.set_ylabel("Axial heat flux (normalized)")
  ax2.set_title("Figure 2: Axial heat flux")
  ax2.legend()
  fig2.tight_layout()
  fig2.savefig(Path(__file__).with_suffix("_heatflux.png"))
  plt.show()


def main() -> None:
  solution = run_simulation()
  plot_thermodynamics(solution)


if __name__ == "__main__":
  main()
