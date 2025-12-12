# pyakiles

Python 3.12 translation of the [AKILES2D MATLAB project](https://github.com/ep2lab/akiles). The code mirrors the
MATLAB package structure at `src/akiles2d` and provides typed
implementations plus pytest-based tests.

## Purpose

The main purpose of this repository is to rewrite the original MATLAB code in Python to enable modern software engineering practices. Specifically, this allows building a CI/CD pipeline to compare results between the original MATLAB implementation and the new Python translation, ensuring accuracy and regression testing.

Additionally, this repository contains a few examples in `examples/python` that attempt to reproduce results from the main paper of the original authors.

## Layout

- Core package: `src/akiles2d/`
- MATLAB-oriented tests: `matlab_port/tests_matlab/`
- Python tests: `tests/`
- Original MATLAB source: `matlab_port/src/+akiles2d/`
- Python translation examples: `examples/python/`

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

## Credits and Legal

This project is a Python translation of the **AKILES2D** code originally developed by **Mario Merino** and **Javier Mauriño**.

### License
The original code and this translation are released under the [MIT License](LICENSE.md).
Copyright (c) 2017 Mario Merino and Javier Mauriño.

### Acknowledging
If you use this code found in the `matlab_port` directory or its translation, please acknowledge the original authors by citing the main article:

> Mario Merino, Javier Mauriño, Eduardo Ahedo, "Kinetic electron model for plasma thruster plumes," Plasma Sources Science and Technology 27, 035013 (2018), [DOI: 10.1088/1361-6595/aab3a1](https://doi.org/10.1088/1361-6595/aab3a1)

and/or the code directly:

> Mario Merino, Javier Mauriño (2017). Akiles2d code: Advanced Kinetic Iterative pLasma Expansion Solver 2D, [DOI: 10.5281/zenodo.1098432](https://doi.org/10.5281/zenodo.1098432)
