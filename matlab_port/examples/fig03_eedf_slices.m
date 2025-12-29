% FIGURE 3 (approximate) from "Kinetic electron model for plasma thruster plumes" (2018)
% Electron energy distribution function sampled at three axial locations using the
% AKILES2D MATLAB port. Energies and distribution values come directly from the
% built-in EEDF postprocessor; the grid is shortened for fast execution.

function fig03_eedf_slices()
  addpath(fullfile(pwd, 'matlab_port'));
  addpath(fullfile(pwd, 'matlab_port', 'src'));

  % Use default configuration
  userdata = akiles2d.simrc();
  userdata.akiles2d.simdir = fullfile(pwd, 'matlab_port', 'examples', 'sims_fig03');
  if ~exist(userdata.akiles2d.simdir, 'dir'); mkdir(userdata.akiles2d.simdir); end
  userdata.akiles2d.datafile = fullfile(userdata.akiles2d.simdir, 'data.mat');

  % Override solver settings to match Python defaults
  userdata.akiles2d.maxiter = 5;
  userdata.akiles2d.tolerance = 2e-2;
  userdata.solver.phibracket = [-10.0, 0.0];

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
  xlim([0, 20]);
  ylim([1e-13, 1e2]);
  xlabel('Electron energy E (normalized)');
  ylabel('EEDF (a.u.)');
  title('Figure 3: EEDF along plume');
  legend('Location', 'southwest');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig03_eedf_slices.png'));

  % Save results for CI comparison
  results.h_indices = idx(:)' - 1; % Convert to 0-based indexing for Python consistency
  results.h_values = sol.h(idx);
  
  % Handle inf in h if present
  if isinf(results.h_values(end))
      results.h_values = num2cell(results.h_values);
      results.h_values{end} = 'inf';
  end

  % Extract slices
  for k = 1:length(idx)
      results.Ek{k} = sol.electrons.Ek(idx(k), :);
      results.EEDF{k} = sol.electrons.EEDF(idx(k), :);
  end

  fid = fopen(fullfile(userdata.akiles2d.simdir, 'fig03_results.json'), 'w');
  if fid == -1, error('Cannot create JSON file'); end
  fwrite(fid, jsonencode(results, 'PrettyPrint', true));
  fclose(fid);
end
