import testrunner
testRunner = testrunner.TestRunner()
testRunner.setGlobalsDictionary(globals())

testSuite1 = testRunner.getOrCreateTestSuite("Question 1")
testSuite1.getOrCreateTestCase("x == 42")
testSuite1.getOrCreateTestCase("x != 43")
testSuite1.getOrCreateTestCase("z == 42")
testSuite1.run()

testSuite2 = testRunner.getOrCreateTestSuite("Question 2")
testSuite2.getOrCreateTestCase("addition(1, 1) == 2")
testSuite2.run()

testRunner.run()