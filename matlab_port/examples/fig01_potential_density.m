% FIGURE 1 (approximate) from "Kinetic electron model for plasma thruster plumes" (2018)
% On-axis potential and density profiles computed with the AKILES2D MATLAB port.
% The grid and integration settings are reduced for faster execution compared to
% the article figures.

function fig01_potential_density()
  % Ensure we can find the package. If run from repo root, 'matlab_port' is enough.
  % If run from inside examples, we need to go up.
  if exist('matlab_port', 'dir')
      addpath(fullfile(pwd, 'matlab_port'));
  elseif exist(fullfile('..', '..', 'matlab_port'), 'dir')
      addpath(fullfile(pwd, '..', '..', 'matlab_port'));
  end

  % Use default configuration from the library
  userdata = akiles2d.simrc();
  
  % Override simulation directory only
  userdata.akiles2d.simdir = fullfile(pwd, 'sims_fig01');
  if ~exist(userdata.akiles2d.simdir, 'dir')
      mkdir(userdata.akiles2d.simdir);
  end
  userdata.akiles2d.datafile = fullfile(userdata.akiles2d.simdir, 'data.mat');
  
  % Override solver settings to match Python defaults
  userdata.akiles2d.maxiter = 5;
  userdata.akiles2d.tolerance = 1e-4;
  userdata.solver.phibracket = [-10.0, 0.0];

  [~, sol] = akiles2d.akiles2d([], userdata);

  figure(1); clf;
  yyaxis left;
  plot(sol.h, sol.phi, 'LineWidth', 1.3);
  ylabel('\phi (V)');
  xlabel('Normalized position h');
  title('Figure 1: potential and density along plume');
  yyaxis right;
  plot(sol.h, sol.electrons.n, '--', 'LineWidth', 1.3); hold on;
  plot(sol.h, sol.ions.n, ':', 'LineWidth', 1.3);
  ylabel('Density (normalized)');
  legend({'\phi', 'n_e', 'n_i'}, 'Location', 'northeast');
  saveas(gcf, fullfile(userdata.akiles2d.simdir, 'fig01_potential_density.png'));

  % Save results for CI comparison
  results.h = sol.h(:)';
  results.phi = sol.phi(:)';
  results.ne = sol.electrons.n(:)';
  results.ni = sol.ions.n(:)';
  
  if isinf(results.h(end))
      % Convert to cell array to allow mixed types (numbers and string "inf")
      results.h = num2cell(results.h);
      results.h{end} = 'inf';
  end
  
  fid = fopen(fullfile(userdata.akiles2d.simdir, 'fig01_results.json'), 'w');
  if fid == -1, error('Cannot create JSON file'); end
  fwrite(fid, jsonencode(results, 'PrettyPrint', true));
  fclose(fid);
end
