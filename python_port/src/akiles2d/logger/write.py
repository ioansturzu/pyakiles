"""Translation of ``+akiles2d/+logger/write.m``."""

from __future__ import annotations

from ..simrc import LoggerConfig
from .log import _wrap_message


def write(message: str, priority: int, logoptions: LoggerConfig) -> None:
  """Write an untagged message respecting debug levels."""

  lines = _wrap_message(message, logoptions.linelength, 28)

  if priority >= logoptions.filedebuglevel:
    with open(logoptions.logfile, "a", encoding="utf-8") as fid:
      for chunk in lines:
        fid.write(f"{'':28}{chunk}\n")

  if priority >= logoptions.screendebuglevel:
    for chunk in lines:
      print(f"{'':28}{chunk}")

