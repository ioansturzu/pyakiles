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

  npoints = 80;
  h = [linspace(1, 4, npoints - 1), inf];
  r = zeros(1, npoints);
  phi_guess = linspace(0, -3, npoints);
  % Get default guess from simrc
  d = akiles2d.simrc();
  guess = d.guess;
  guess.h = h(:);
  guess.r = r(:);
  guess.phi = phi_guess(:);
  guess.ne00p = 0.5;

  userdata.guess = guess;
  userdata.electrons.model = 'semimaxwellian';
  userdata.electrons.nintegrationpoints = [80, 40];
  
  % Set simulation directory relative to current location
  userdata.akiles2d.simdir = fullfile(pwd, 'sims_fig01');
  if ~exist(userdata.akiles2d.simdir, 'dir')
      mkdir(userdata.akiles2d.simdir);
  end

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

  % Save results for CI comparison
  results.h = sol.h(:)';
  results.phi = sol.phi(:)';
  results.ne = sol.electrons.n(:)';
  results.ni = sol.ions.n(:)';
  
  if isinf(results.h(end))
      % Replace inf with "inf" string for JSON consistency or handle in reader
      % MATLAB jsonencode handles Inf as null or similar depending on version,
      % but let's stringify or just leave it and handle in Python
      results.h(end) = 1e308; % Use large number as placeholder if needed, or rely on Python reader
      % Actually, let's just use a struct and jsonencode
  end
  
  fid = fopen(fullfile(userdata.akiles2d.simdir, 'fig01_results.json'), 'w');
  if fid == -1, error('Cannot create JSON file'); end
  fwrite(fid, jsonencode(results));
  fclose(fid);
end
