PyAKILES: A Python Port of AKILES2D
====================================

**PyAKILES** is a faithful Python translation of the [AKILES2D MATLAB library](https://github.com/mmerino/akiles2d), originally developed by Mario Merino. It simulates the kinetic behavior of electrons in plasma thruster plumes/expansions using a semi-analytical approach.

Original Project & Reference
----------------------------

The original MATLAB implementation, **AKILES2D**, is described in the following paper:

> **Mario Merino and Eduardo Ahedo**, "Kinetic electron model for plasma thruster plumes", *Plasma Sources Science and Technology*, 2018.

### Abstract (from the paper)

> *A fully kinetic model for the electrons in the unmagnetized plume of a plasma thruster is developed. The model takes advantage of the different time scales of the electron motion to average the Vlasov equation over the fast electron bounce motion in the ambipolar electric potential well. This reduces the problem to a 1D integro-differential equation for the electron energy distribution function (EEDF) along the magnetic field lines (or streamtubes). The model includes the effect of electron-neutral and electron-ion collisions, as well as the emission of secondary electrons from the thruster walls. The model is applied to a divergent magnetic nozzle, and the results are compared with fluid and hybrid simulations.*

### Main Features (MATLAB Version)

The original library employs a specialized kinetic solver that:

1.  Assumes electrons are magnetized or confined by the ambipolar potential, allowing bounce-averaging of the Vlasov equation.
2.  Discretizes the electron distribution function (EDF) in total energy ($\varepsilon$) and magnetic moment ($\mu$).
3.  Solving for the electrostatic potential $\phi(h)$ that satisfies quasineutrality given ion density profiles map.
4.  Computing moments of the distribution function (density, temperature, heat flux) efficiently.

Relevant equations typically solved include the quasineutrality condition:

$$ n_e(\phi) = n_i(\phi) $$

Where electron density $n_e$ is an integral over the distribution function $f(\varepsilon, \mu)$.

Rationale for Python Translation
--------------------------------

While MATLAB is powerful for prototyping, the Python ecosystem offers several advantages for modern scientific computing workflows:

*   **Open Source & Accessibility:** No license costs, making the code accessible to a broader community.
*   **Integration:** Easier integration with machine learning frameworks (PyTorch, JAX), web services, and cloud-based CI/CD pipelines.
*   **Performance:** Utilization of JIT compilation (via **Numba**) to approach or exceed compiled language performance for heavy numerical loops.
*   **Ecosystem:** Access to rich libraries like `scipy`, `xarray`, and `matplotlib` for analysis and visualization.

This port aims to be **numerically equivalent** to the MATLAB original while adopting Pythonic best practices (packaging, typing, testing).

Examples & Validation
---------------------

This documentation includes comparisons of three key physical scenarios to validate the Python port against the original MATLAB baseline. Comparison plots are generated automatically by the CI pipeline.

### 1. Potential and Density Profiles

This example computes the self-consistent electrostatic potential $\phi(h)$ and resulting electron/ion densities along the plume axis.

**Python Code:** `examples/potential_density.py`

```{eval-rst}
.. literalinclude:: ../examples/potential_density.py
   :language: python
   :caption: potential_density.py
```

```{image} images/potential_density.png
   :alt: Potential and Density Comparison
   :width: 80%
   :align: center
```

### 2. Thermodynamics (Temperature & Heat Flux)

Here we analyze the evolution of parallel and perpendicular electron temperatures ($T_{\parallel}, T_{\perp}$) and the axial heat flux $q_z$.

**Python Code:** `examples/temperature_heatflux.py`

```{eval-rst}
.. literalinclude:: ../examples/temperature_heatflux.py
   :language: python
   :caption: temperature_heatflux.py
```

```{image} images/temperature_heatflux_temps.png
   :alt: Thermodynamics Comparison
   :width: 80%
   :align: center
```

### 3. Electron Energy Distribution Function (EEDF)

This example visualizes the Electron Energy Distribution Function at various points along the plume, showing the evolution from a Maxwellian source to a non-equilibrium distribution downstream.

**Python Code:** `examples/eedf_slices.py`

```{eval-rst}
.. literalinclude:: ../examples/eedf_slices.py
   :language: python
   :caption: eedf_slices.py
```

```{image} images/eedf_slices.png
   :alt: EEDF Comparison
   :width: 80%
   :align: center
```

Running the Comparisons
-----------------------

To generate the comparison plots locally (assuming you have the results JSONs from running the examples):

```bash
uv run docs/scripts/generate_plots.py
```

Comparison Logic
----------------

The validation scripts compare raw numerical outputs (JSON) from both implementations. Tolerance thresholds are set (typically around 5%) to account for:

*   Differences in root-finding algorithms (`fzero` vs `scipy.optimize.brentq`).
*   Floating point arithmetic differences between engines.
*   Handling of `Inf` and edge cases in integration grids.

Despite these minor numerical differences, the physics trends and magnitudes are consistently reproduced.
