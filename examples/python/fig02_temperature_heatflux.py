"""
Example script mirroring the AKILES2D figure 02 thermodynamics plot.

Running this module executes the default AKILES2D simulation and saves two
figures: one for electron/ion temperatures and another for the axial heat flux
components. Outputs are written next to this file with ``_temps`` and
``_heatflux`` suffixes.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from akiles2d.akiles2d import akiles2d


def plot_thermodynamics(solution: dict[str, object]) -> None:
  r = np.asarray(solution["r"])
  electrons = solution["electrons"]
  ions = solution["ions"]

  temp_fig, temp_ax = plt.subplots(figsize=(5, 4))
  temp_ax.plot(r, electrons["Tz"], label="Tz_e")
  temp_ax.plot(r, electrons["Tr"], label="Tr_e")
  temp_ax.plot(r, ions["Tz"], label="Tz_i")
  temp_ax.set_xlabel("r")
  temp_ax.set_ylabel("Temperature")
  temp_ax.legend()

  heat_fig, heat_ax = plt.subplots(figsize=(5, 4))
  heat_ax.plot(r, electrons["qzz"], label="qzz_e")
  heat_ax.plot(r, electrons["qzr"], label="qzr_e")
  heat_ax.plot(r, ions["qzz"], label="qzz_i")
  heat_ax.set_xlabel("r")
  heat_ax.set_ylabel("Heat flux")
  heat_ax.legend()

  temps_path = Path(__file__).with_name(Path(__file__).stem + "_temps.png")
  heatflux_path = Path(__file__).with_name(Path(__file__).stem + "_heatflux.png")
  temp_fig.savefig(temps_path)
  heat_fig.savefig(heatflux_path)


def main() -> None:
  _, solution = akiles2d()
  plot_thermodynamics(solution)


if __name__ == "__main__":
  main()
