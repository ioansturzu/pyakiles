function tests = test_akiles2d_main
% Smoke test for akiles2d main entry point.
tests = functiontests(localfunctions);

function testMainRunsOneIteration(testCase)
  simdir = fullfile(tempdir,'akiles2d_main');
  userdata.akiles2d = akiles2d.simrc().akiles2d;
  userdata.akiles2d.simdir = simdir;
  userdata.akiles2d.maxiter = 0;
  userdata.guess = akiles2d.simrc().guess;
  userdata.guess.h = [1;2];
  userdata.guess.r = [0;0];
  userdata.guess.phi = [0;-0.1];
  userdata.guess.ne00p = 0.2;
  [data,solution] = akiles2d.akiles2d([],userdata);
  verifyEqual(testCase,solution.npoints,2);
  verifyTrue(testCase,isfolder(simdir));
end

end
