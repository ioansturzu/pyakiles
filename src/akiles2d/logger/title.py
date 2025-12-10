"""Translation of ``+akiles2d/+logger/title.m``."""

from __future__ import annotations

from ..simrc import LoggerConfig


def _divider(length: int) -> str:
  return "-" * max(70, length)


def title(message: str, priority: int, logoptions: LoggerConfig) -> None:
  """Write a title-style log entry with horizontal dividers."""

  lines = [message[i : i + (max(70, logoptions.linelength) - 20)] for i in range(0, len(message), max(70, logoptions.linelength) - 20)] or [""]
  divider = _divider(logoptions.linelength)

  if priority >= logoptions.filedebuglevel:
    with open(logoptions.logfile, "a", encoding="utf-8") as fid:
      fid.write("\n")
      fid.write(f"{divider}\n")
      for chunk in lines:
        fid.write(f"{'':10}{chunk}\n")
      fid.write(f"{divider}\n\n")

  if priority >= logoptions.screendebuglevel:
    print()
    print(divider)
    for chunk in lines:
      print(f"{'':10}{chunk}")
    print(divider)
    print()

