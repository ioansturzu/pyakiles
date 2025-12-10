function tests = test_solver_solver
% Migration tests for solver sweep.
tests = functiontests(localfunctions);

function testSolverAdjustsPhi(testCase)
  data = akiles2d.simrc();
  data.solver.phibracket = [-1, 0.1];
  solution.h = [1; 2];
  solution.r = [0; 0];
  solution.phi = [0; -0.1];
  solution.ne00p = data.guess.ne00p;
  solution.npoints = numel(solution.h);
  solution.errorfcn = [0.2; 0.1];
  updated = akiles2d.solver.solver(data,solution);
  verifyEqual(testCase,numel(updated.phi),solution.npoints);
end

end
