from pathlib import Path

from akiles2d.logger import blank, log, title, write
from akiles2d.simrc import LoggerConfig


def test_logger_writes(tmp_path: Path):
  logfile = tmp_path / "log.txt"
  opts = LoggerConfig(logfile=str(logfile), screendebuglevel=10, filedebuglevel=0, linelength=80)
  title("Test Title", 1, opts)
  log("hello", "INF", 1, opts)
  write("details", 1, opts)
  blank(1, opts)
  assert logfile.exists()

