function tests = test_electrons_semimaxwellian
% Migration tests for semimaxwellian electron routines.
tests = functiontests(localfunctions);

function testMomentTrivial(testCase)
  data = akiles2d.simrc();
  data.guess.h = [1;2];
  data.guess.r = [0;0];
  data.guess.phi = [0;-1];
  solution = data.guess;
  solution.npoints = numel(solution.h);
  [m,~,~,~] = akiles2d.electrons.parabolic.semimaxwellian.moment(data,solution,0,1,0);
  verifyEqual(testCase,m,zeros(size(solution.h)));
end

function testNe00pPhiinfty(testCase)
  [ne00p,phiinfty] = akiles2d.electrons.parabolic.semimaxwellian.ne00p_phiinfty_nobarriers(0.02);
  verifyLessThan(testCase,phiinfty,0);
  verifyGreaterThan(testCase,ne00p,0);
end

end
