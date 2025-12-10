"""Translation of ``+akiles2d/+logger/blank.m``."""

from __future__ import annotations

from ..simrc import LoggerConfig


def blank(priority: int, logoptions: LoggerConfig) -> None:
  """Emit a blank line to log destinations when permitted by priority."""

  if priority >= logoptions.filedebuglevel:
    with open(logoptions.logfile, "a", encoding="utf-8") as fid:
      fid.write("\n")
  if priority >= logoptions.screendebuglevel:
    print()

