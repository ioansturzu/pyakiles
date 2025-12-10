function tests = test_ions_cold
% Migration tests for cold ion moment function.
tests = functiontests(localfunctions);

function testMomentAxis(testCase)
  data = akiles2d.simrc();
  data.ions.mu = 10;
  solution.h = [1;1.5];
  solution.r = [0;0];
  solution.phi = [0;-0.2];
  [m,~,~,~] = akiles2d.ions.parabolic.cold.moment(data,solution,0,0,0);
  verifyEqual(testCase,numel(m),2);
  verifyGreaterThan(testCase,m(1),0);
end

function testMomentOffAxisError(testCase)
  data = akiles2d.simrc();
  solution.h = [1;1.5];
  solution.r = [0;0.1];
  solution.phi = [0;-0.2];
  verifyError(testCase,@() akiles2d.ions.parabolic.cold.moment(data,solution,0,0,0), '');
end

end
