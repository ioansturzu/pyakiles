# pyakiles

Python 3.12 translation of the AKILES2D MATLAB project. The code mirrors the
MATLAB package structure at `src/akiles2d` and provides typed
implementations plus pytest-based tests.

## Layout

- Core package: `src/akiles2d/`
- MATLAB-oriented tests: `matlab_port/tests_matlab/`
- Python tests: `tests/`
- Original MATLAB source: `matlab_port/src/+akiles2d/`

## Usage with uv

```bash
cd python_port
uv sync
uv run pytest
```

To run the simulation entry point:

```bash
uv run -m akiles2d.akiles2d
```

MATLAB tests mirror the Python tests for migration verification and live in
`matlab_port/tests_matlab/`. They can be executed with MATLAB's `runtests` command.

