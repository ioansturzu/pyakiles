% FIGURE 2 (approximate) from "Kinetic electron model for plasma thruster plumes" (2018)
% Parallel/perpendicular electron temperatures and axial heat flux obtained from
% AKILES2D kinetic moments with a reduced grid for quick visualization.

function fig02_temperature_heatflux(test_mode)
  if ~exist('test_mode', 'var')
      test_mode = false;
  end

  addpath(fullfile(pwd, 'matlab_port'));
  addpath(fullfile(pwd, 'matlab_port', 'src'));

  % Use default configuration
  userdata = akiles2d.simrc();
  userdata.akiles2d.simdir = fullfile(pwd, 'matlab_port', 'examples', 'sims_fig02');
  if ~exist(userdata.akiles2d.simdir, 'dir'); mkdir(userdata.akiles2d.simdir); end
  userdata.akiles2d.datafile = fullfile(userdata.akiles2d.simdir, 'data.mat');
  
  if test_mode
      disp('Running in TEST mode (npoints=50)');
      npoints = 50;
      userdata.guess.h = [linspace(1,5,npoints-1),Inf].'; 
      userdata.guess.r = zeros(1,npoints).'; 
      userdata.guess.phi = linspace(0,-4,npoints).';
  end

  % Override solver settings to match Python defaults
  userdata.akiles2d.maxiter = 5;
  userdata.akiles2d.tolerance = 2e-2;
  userdata.solver.phibracket = [-10.0, 0.0];
  % Ensure moments postprocessor is active (it is by default but being explicit is fine)
  userdata.postprocessor.postfunctions = {'moments'};

  [~, sol] = akiles2d.akiles2d([], userdata);

  figure(1); clf;
  plot(sol.h, sol.electrons.Tz, 'LineWidth', 1.3); hold on;
  plot(sol.h, sol.electrons.Tr, '--', 'LineWidth', 1.3);
  xlabel('Normalized position h');
  ylabel('Temperature (normalized)');
  legend({'T_{||}', 'T_{\perp}'}, 'Location', 'northeast');
  idx_finite = ~isinf(sol.h);
  xlim([1, max(sol.h(idx_finite))]);
  title('Figure 2: electron temperatures');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig02_temperatures.png'));

  figure(2); clf;
  plot(sol.h, sol.electrons.qzz, 'LineWidth', 1.3);
  xlabel('Normalized position h');
  ylabel('Axial heat flux q_z');
  xlim([1, max(sol.h(idx_finite))]);
  title('Figure 2: axial heat flux');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig02_heatflux.png'));

  % Save results for CI comparison
  results.r = sol.r(:)';
  results.Tz_e = sol.electrons.Tz(:)';
  results.Tr_e = sol.electrons.Tr(:)';
  results.Tz_i = sol.ions.Tz(:)';
  results.qzz_e = sol.electrons.qzz(:)';
  results.qzr_e = sol.electrons.qzr(:)';
  results.qzz_i = sol.ions.qzz(:)';

  fid = fopen(fullfile(userdata.akiles2d.simdir, 'fig02_results.json'), 'w');
  if fid == -1, error('Cannot create JSON file'); end
  fwrite(fid, jsonencode(results, 'PrettyPrint', true));
  fclose(fid);
end
