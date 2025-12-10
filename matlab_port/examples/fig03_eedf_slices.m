% FIGURE 3 (approximate) from "Kinetic electron model for plasma thruster plumes" (2018)
% Electron energy distribution function sampled at three axial locations using the
% AKILES2D MATLAB port. Energies and distribution values come directly from the
% built-in EEDF postprocessor; the grid is shortened for fast execution.

function fig03_eedf_slices()
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
  userdata.akiles2d.simdir = fullfile(pwd, 'matlab_port', 'examples', 'sims_fig03');
  userdata.akiles2d.maxiter = 3;
  userdata.akiles2d.tolerance = 1e-3;
  userdata.akiles2d.datafile = fullfile(userdata.akiles2d.simdir, 'data.mat');
  userdata.postprocessor.postfunctions = {'moments', 'EEDF'};

  [~, sol] = akiles2d.akiles2d([], userdata);

  idx = [1, floor(length(sol.h)/2), length(sol.h)-1];
  labels = {'Injection', 'Mid plume', 'Far plume'};

  figure(1); clf;
  hold on;
  for k = 1:length(idx)
    plot(sol.electrons.Ek(idx(k), :), sol.electrons.EEDF(idx(k), :), 'DisplayName', ...
      sprintf('%s (h=%.2f)', labels{k}, sol.h(idx(k))));
  end
  set(gca, 'YScale', 'log');
  xlabel('Electron energy E (normalized)');
  ylabel('EEDF (a.u.)');
  title('Figure 3: EEDF along plume');
  legend('Location', 'southwest');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig03_eedf_slices.png'));
end
