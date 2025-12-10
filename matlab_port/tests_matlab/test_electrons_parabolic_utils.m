function tests = test_electrons_parabolic_utils
% Migration-oriented tests for parabolic electron helper functions.
tests = functiontests(localfunctions);

function testUeffAndVelocities(testCase)
  h = 2;
  phiz = -0.5;
  Jr = 0.2;
  ptheta = 0.1;
  U = akiles2d.electrons.parabolic.Ueff(h,phiz,Jr,ptheta);
  verifyGreaterThan(testCase,U,0);

  [vz,vr,vtheta] = akiles2d.electrons.parabolic.getvelocities(h,1,phiz,1,Jr,ptheta);
  verifySize(testCase,vz,[1 1]);
  verifyGreaterThan(testCase,vz,0);
  verifyGreaterThanOrEqual(testCase,vtheta,0);
end

function testBetarRoundTrip(testCase)
  h = [1;2];
  betar = [0;0.25];
  Jr = [0.1;0.2];
  ptheta = [0.0;0.05];
  r = akiles2d.electrons.parabolic.getr(h,betar,Jr,ptheta);
  betar2 = akiles2d.electrons.parabolic.getbetar(h,r,Jr,ptheta);
  verifyLessThan(testCase,max(abs(betar2-betar)),1e-10);
end

function testMomenta(testCase)
  h = [1;1.5];
  r = [0;0.2];
  phiz = [0;-0.2];
  vz = [0.5;0.7];
  vr = [0.1;0.2];
  vtheta = [0.0;0.05];
  [E,Jr,ptheta] = akiles2d.electrons.parabolic.getmomenta(h,r,phiz,vz,vr,vtheta);
  verifyEqual(testCase,ptheta(1),0);
  verifySize(testCase,E,size(h));
  verifyGreaterThan(testCase,Jr(2),0);
end

end
