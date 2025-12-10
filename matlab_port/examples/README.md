# MATLAB figure reproductions

Approximate reproductions of the figures from *Kinetic electron model for plasma thruster plumes* (2018) using the MATLAB AKILES2D port. Add `matlab_port/` to your MATLAB path and run from the repository root.

- `fig01_potential_density.m` — Figure 1: axial potential plus electron/ion densities (reduced resolution for speed).
- `fig02_temperature_heatflux.m` — Figure 2: electron parallel/perpendicular temperatures and axial heat flux.
- `fig03_eedf_slices.m` — Figure 3: electron energy distribution functions sampled at three axial locations.

## Usage

In MATLAB:

```matlab
addpath(fullfile(pwd, 'matlab_port'));
addpath(fullfile(pwd, 'matlab_port', 'src'));
fig01_potential_density;
fig02_temperature_heatflux;
fig03_eedf_slices;
```

Each script writes PNG outputs inside `matlab_port/examples/sims_figNN/` alongside solver iteration files.
