# Python figure reproductions

Example scripts that approximate the figures from *Kinetic electron model for plasma thruster plumes* (2018) using the Python AKILES2D port. Run each from the repository root so that `src` is on the Python path.

- `fig01_potential_density.py` — Figure 1: axial potential and electron/ion density profiles (reduced grid for speed).
- `fig02_temperature_heatflux.py` — Figure 2: parallel/perpendicular electron temperatures and axial heat flux derived from kinetic moments.
- `fig03_eedf_slices.py` — Figure 3: electron energy distribution functions at representative axial positions.

## Usage

```bash
python examples/python/fig01_potential_density.py
python examples/python/fig02_temperature_heatflux.py
python examples/python/fig03_eedf_slices.py
```

Each script saves a PNG next to the source file and stores intermediate solver
outputs under `examples/python/sims_figNN/`.
