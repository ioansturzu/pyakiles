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
import sys

# Ensure the local source tree is importable when executed from the repo root.
sys.path.append("src")

from akiles2d.akiles2d import akiles2d


def plot_thermodynamics(solution: dict[str, object]) -> None:
  h = np.asarray(solution["h"], dtype=float)
  
  # Compute axial position z from metric factor h
  # dz/dxi = h, so z = integral(h dxi). On uniform grid dxi=1?? 
  # Actually usually z is just the coordinate if h is constant, but h varies.
  # Let's check fig01 logic. fig01 plots vs h directly? No, fig01 plots vs h.
  # The article plots vs z. z is related to h.
  # For the purpose of meaningful plots, we should plot vs h (normalized coordinate) 
  # or derived z. Since fig01 uses h, let's consistency use h like fig01.
  # The previous "dumb" plot used 'r', which is 0.
  
  metric_h = h[:-1] # Last point is inf
  # Let's just plot vs index or 'h' value like fig01.
  x_axis = h
  x_label = "Normalized position h"
  
  # Or better: z.
  # If we really want physical Z, it's cumulative sum of h * dxi.
  # But simple h is sufficient to show the profile structure.
  
  electrons = solution["electrons"]
  ions = solution["ions"]

  temp_fig, temp_ax = plt.subplots(figsize=(5, 4))
  temp_ax.plot(x_axis, electrons["Tz"], label="Tz_e")
  temp_ax.plot(x_axis, electrons["Tr"], label="Tr_e")
  temp_ax.plot(x_axis, ions["Tz"], label="Tz_i")
  temp_ax.set_xlabel(x_label)
  temp_ax.set_ylabel("Temperature")
  temp_ax.set_ylabel("Temperature")
  temp_ax.set_xlim(left=1.0, right=max(x_axis[x_axis<np.inf])) # Start exactly at 1.0
  temp_ax.legend()

  heat_fig, heat_ax = plt.subplots(figsize=(5, 4))
  heat_ax.plot(x_axis, electrons["qzz"], label="qzz_e")
  heat_ax.plot(x_axis, electrons["qzr"], label="qzr_e")
  heat_ax.plot(x_axis, ions["qzz"], label="qzz_i")
  heat_ax.set_xlabel(x_label)
  heat_ax.set_ylabel("Heat flux")
  heat_ax.set_xlim(left=1.0, right=max(x_axis[x_axis<np.inf]))
  heat_ax.legend()

  temps_path = Path(__file__).with_name(Path(__file__).stem + "_temps.png")
  heatflux_path = Path(__file__).with_name(Path(__file__).stem + "_heatflux.png")
  temp_fig.savefig(temps_path)
  heat_fig.savefig(heatflux_path)


from akiles2d.simrc import Akiles2DConfig, PostprocessorConfig

def run_simulation() -> dict:
  """Run the standard AKILES2D solve (default parameters)."""
  simdir = Path("examples/python/sims_fig02")
  
  # Configure simulation directory
  userdata = {
    "akiles2d": Akiles2DConfig(simdir=str(simdir), datafile=str(simdir / "data.mat")),
    "postprocessor": PostprocessorConfig(postfunctions=["moments"]),
  }
  
  _, solution = akiles2d(userdata=userdata)
  return solution

def main() -> None:
  solution = run_simulation()
  plot_thermodynamics(solution)

  # Save results for CI comparison
  import json
  
  electrons = solution["electrons"]
  ions = solution["ions"]
  results = {
      "r": np.asarray(solution["r"], dtype=float).tolist(),
      "Tz_e": np.asarray(electrons["Tz"], dtype=float).tolist(),
      "Tr_e": np.asarray(electrons["Tr"], dtype=float).tolist(),
      "Tz_i": np.asarray(ions["Tz"], dtype=float).tolist(),
      "qzz_e": np.asarray(electrons["qzz"], dtype=float).tolist(),
      "qzr_e": np.asarray(electrons["qzr"], dtype=float).tolist(),
      "qzz_i": np.asarray(ions["qzz"], dtype=float).tolist(),
  }

  with open(Path(__file__).with_name("fig02_results.json"), "w") as f:
      json.dump(results, f, indent=2)


if __name__ == "__main__":
  main()
