function tests = test_preprocessor
% Migration tests for preprocessor overrides.
tests = functiontests(localfunctions);

function testOverrideLogfile(testCase)
  simdir = fullfile(tempdir,'akiles2d_test');
  userdata.akiles2d = akiles2d.simrc().akiles2d;
  userdata.akiles2d.simdir = simdir;
  data = akiles2d.preprocessor.preprocessor([],userdata);
  verifyTrue(testCase,contains(data.logger.logfile,simdir));
end

end
