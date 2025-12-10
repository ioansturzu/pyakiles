% FIGURE 1 (approximate) from "Kinetic electron model for plasma thruster plumes" (2018)
% On-axis potential and density profiles computed with the AKILES2D MATLAB port.
% The grid and integration settings are reduced for faster execution compared to
% the article figures.

function fig01_potential_density()
  addpath(fullfile(pwd, 'matlab_port'));
  addpath(fullfile(pwd, 'matlab_port', 'src'));

  npoints = 80;
  h = [linspace(1, 4, npoints - 1), inf];
  r = zeros(1, npoints);
  phi_guess = linspace(0, -3, npoints);
  guess = akiles2d.simrc.default_guess();
  guess.h = h(:);
  guess.r = r(:);
  guess.phi = phi_guess(:);
  guess.ne00p = 0.5;

  userdata.guess = guess;
  userdata.electrons.model = 'semimaxwellian';
  userdata.electrons.nintegrationpoints = [80, 40];
  userdata.akiles2d.simdir = fullfile(pwd, 'matlab_port', 'examples', 'sims_fig01');
  userdata.akiles2d.maxiter = 3;
  userdata.akiles2d.tolerance = 1e-3;
  userdata.akiles2d.datafile = fullfile(userdata.akiles2d.simdir, 'data.mat');
  userdata.postprocessor.postfunctions = {'moments', 'EEDF'};

  [~, sol] = akiles2d.akiles2d([], userdata);

  figure(1); clf;
  yyaxis left;
  plot(sol.h, sol.phi, 'LineWidth', 1.3);
  ylabel('\phi (V)');
  xlabel('Normalized position h');
  title('Figure 1: potential and density along plume');
  yyaxis right;
  plot(sol.electrons.n, '--', 'LineWidth', 1.3); hold on;
  plot(sol.ions.n, ':', 'LineWidth', 1.3);
  ylabel('Density (normalized)');
  legend({'\phi', 'n_e', 'n_i'}, 'Location', 'northeast');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig01_potential_density.png'));
end
