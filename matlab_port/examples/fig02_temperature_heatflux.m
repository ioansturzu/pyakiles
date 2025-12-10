% FIGURE 2 (approximate) from "Kinetic electron model for plasma thruster plumes" (2018)
% Parallel/perpendicular electron temperatures and axial heat flux obtained from
% AKILES2D kinetic moments with a reduced grid for quick visualization.

function fig02_temperature_heatflux()
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
  userdata.akiles2d.simdir = fullfile(pwd, 'matlab_port', 'examples', 'sims_fig02');
  userdata.akiles2d.maxiter = 3;
  userdata.akiles2d.tolerance = 1e-3;
  userdata.akiles2d.datafile = fullfile(userdata.akiles2d.simdir, 'data.mat');
  userdata.postprocessor.postfunctions = {'moments', 'EEDF'};

  [~, sol] = akiles2d.akiles2d([], userdata);

  figure(1); clf;
  plot(sol.h, sol.electrons.Tz, 'LineWidth', 1.3); hold on;
  plot(sol.h, sol.electrons.Tr, '--', 'LineWidth', 1.3);
  xlabel('Normalized position h');
  ylabel('Temperature (normalized)');
  legend({'T_{||}', 'T_{\perp}'}, 'Location', 'northeast');
  title('Figure 2: electron temperatures');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig02_temperatures.png'));

  figure(2); clf;
  plot(sol.h, sol.electrons.qzz, 'LineWidth', 1.3);
  xlabel('Normalized position h');
  ylabel('Axial heat flux q_z');
  title('Figure 2: axial heat flux');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig02_heatflux.png'));
end
