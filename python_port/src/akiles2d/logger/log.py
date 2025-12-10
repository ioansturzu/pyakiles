"""Translation of ``+akiles2d/+logger/log.m``."""

from __future__ import annotations

from datetime import datetime

from ..simrc import LoggerConfig


def _wrap_message(message: str, linelength: int, header: int) -> list[str]:
  available = max(70, linelength) - header
  return [message[i : i + available] for i in range(0, len(message), available)] or [""]


def log(message: str, tag: str, priority: int, logoptions: LoggerConfig) -> None:
  """Write a tagged message to the screen and logfile."""

  lines = _wrap_message(message, logoptions.linelength, 28)
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  if priority >= logoptions.filedebuglevel:
    with open(logoptions.logfile, "a", encoding="utf-8") as fid:
      for i, chunk in enumerate(lines):
        if i == 0:
          fid.write(f"[{timestamp}] [{tag[:3]}] {chunk}\n")
        else:
          fid.write(f"{'':28}{chunk}\n")

  if priority >= logoptions.screendebuglevel:
    for i, chunk in enumerate(lines):
      if i == 0:
        print(f"[{timestamp}] [{tag[:3]}] {chunk}")
      else:
        print(f"{'':28}{chunk}")

