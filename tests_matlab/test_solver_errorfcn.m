function tests = test_solver_errorfcn
% Migration tests for solver error function.
tests = functiontests(localfunctions);

function testErrorVectorLength(testCase)
  data = akiles2d.simrc();
  data.ions.mu = 10;
  solution.h = [1; 2];
  solution.r = [0; 0];
  solution.phi = [0; -0.5];
  solution.ne00p = data.guess.ne00p;
  solution.npoints = numel(solution.h);
  err = akiles2d.solver.errorfcn(data,solution);
  verifyEqual(testCase,numel(err),solution.npoints);
end

end
