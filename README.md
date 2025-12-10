# pyakiles

Python 3.12 translation of the AKILES2D MATLAB project. The code mirrors the
MATLAB package structure inside `python_port/src/akiles2d` and provides typed
implementations plus pytest-based tests.

## Layout

- Core package: `python_port/src/akiles2d/`
- MATLAB-oriented tests: `tests_matlab/`
- Python tests: `python_port/tests/`

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
`tests_matlab/`. They can be executed with MATLAB's `runtests` command.

