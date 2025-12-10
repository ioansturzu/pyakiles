function tests = test_potential_phi
% Auto-generated migration test for +akiles2d/+potential/+parabolic/phi.m
tests = functiontests(localfunctions);

function testBasicPhi(testCase)
  h = [1; 2];
  r = [0; 1];
  phiz = [0; -1];
  phiVals = akiles2d.potential.parabolic.phi(h,r,phiz);
  verifyEqual(testCase,phiVals(1),0);
  verifyLessThan(testCase,phiVals(2),phiz(2));
end

end
