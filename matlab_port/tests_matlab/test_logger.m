function tests = test_logger
% Migration tests for logger utilities.
import akiles2d.logger.*
tests = functiontests(localfunctions);

function testLogWritesFile(testCase)
  tmp = fullfile(tempdir,'akiles2d_logger.txt');
  opts.logfile = tmp;
  opts.screendebuglevel = 10;
  opts.filedebuglevel = 0;
  opts.linelength = 80;
  akiles2d.logger.title('Test Title',1,opts);
  akiles2d.logger.log('hello','INF',1,opts);
  akiles2d.logger.write('details',1,opts);
  akiles2d.logger.blank(1,opts);
  verifyTrue(testCase,isfile(tmp));
end

end
