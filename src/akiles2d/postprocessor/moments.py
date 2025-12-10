"""Translation of ``+akiles2d/+postprocessor/moments.m``."""

from __future__ import annotations

import numpy as np

from ..electrons import parabolic as epar
from ..ions import parabolic as ipar
from ..simrc import Data


def moments(data: Data, solution: dict[str, object]) -> dict[str, object]:
  """Compute electron and ion moments and derived quantities."""

  def compute(prefix: str, module) -> None:
    for name, exps in {
      "000": (0, 0, 0),
      "100": (1, 0, 0),
      "200": (2, 0, 0),
      "020": (0, 2, 0),
      "002": (0, 0, 2),
      "300": (3, 0, 0),
      "120": (1, 2, 0),
      "102": (1, 0, 2),
    }.items():
      m, m1, m2, m4 = module.moment(data, solution, *exps)
      solution.setdefault(prefix, {})[f"M{name}"] = m
      solution[prefix][f"M{name}1"] = m1
      solution[prefix][f"M{name}2"] = m2
      solution[prefix][f"M{name}4"] = m4

  compute("electrons", epar.semimaxwellian)
  compute("ions", ipar.cold)

  def derived(prefix: str) -> None:
    ll = ["", "1", "2", "4"]
    for l in ll:
      n = solution[prefix][f"M000{l}"]
      u = np.divide(solution[prefix][f"M100{l}"], n, out=np.zeros_like(n), where=n != 0)
      Tz = np.divide(solution[prefix][f"M200{l}"], n, out=np.zeros_like(n), where=n != 0) - u**2
      Tr = np.divide(solution[prefix][f"M020{l}"], n, out=np.zeros_like(n), where=n != 0)
      Ttheta = np.divide(solution[prefix][f"M002{l}"], n, out=np.zeros_like(n), where=n != 0)
      solution[prefix][f"n{l}"] = n
      solution[prefix][f"u{l}"] = u
      solution[prefix][f"Tz{l}"] = Tz
      solution[prefix][f"Tr{l}"] = Tr
      solution[prefix][f"Ttheta{l}"] = Ttheta
      solution[prefix][f"qzz{l}"] = 0.5 * solution[prefix][f"M300{l}"] - 1.5 * n * u * Tz - 0.5 * n * u**3
      solution[prefix][f"qzr{l}"] = 0.5 * solution[prefix][f"M120{l}"] - 0.5 * n * u * Tr
      solution[prefix][f"qztheta{l}"] = 0.5 * solution[prefix][f"M102{l}"] - 0.5 * n * u * Ttheta

  derived("electrons")
  derived("ions")
  return solution

