#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module introduce a basic test runner inspired from "mocha" output.
"""

__author__ = "Romain Andre-Lovichi"
__licence__ = "GPL"



class TestRunner():
    """A test runner inspired from "mocha" output"""

    def __init__(self):
        """Create a new test runner"""
        self.suites = []

    def createTestSuite(self, suiteName):
        """Create a new test suite"""
        suite = TestSuite(suiteName)
        suite.setGlobalsDictionary(self.globals)
        self.suites.append(suite)
        return suite

    def evaluate(self):
        """Evaluate all test suites"""
        failCount = 0
        for suite in self.suites:
            suite.evaluate()
            if not (suite.success):
                failCount += 1
        self.totalCount = len(self.suites)
        self.failCount = failCount
        self.successCount = self.totalCount - self.failCount

    def getOrCreateTestSuite(self, suiteName):
        """Get a test suite by name, and create it if needed"""
        existingTestSuite = self.getTestSuiteByName(suiteName)
        if (existingTestSuite is not None):
            return existingTestSuite
        return self.createTestSuite(suiteName)

    def getTestSuiteByName(self, name):
        """Get test suite by name"""
        for suite in self.suites:
            if (suite.name == name):
                return suite
        return None

    def printResults(self):
        """Print results in the standard output"""
        for suite in self.suites:
            suite.printResults()
        print()
        print()
        if (self.failCount == 0):
            print("🚀 All {0} tests passed!".format(self.totalCount))
        else:
            print("⚠️ Some test failed!")
            print("    {0} passing".format(self.successCount))
            print("    {0} failing".format(self.failCount))

    def run(self):
        """Run all test suites and print results"""
        self.evaluate()
        self.printResults()

    def setGlobalsDictionary(self, globals):
        """Set the dictionary containing the current scope's global variables"""
        self.globals = globals



class TestSuite():
    """A test suite is a group of related test cases"""

    def __init__(self, name):
        """Create a new test suite"""
        self.name = name
        self.cases = []

    def createTestCase(self, expressionToEvaluate):
        """Create a new test case"""
        case = TestCase(expressionToEvaluate)
        case.setGlobalsDictionary(self.globals)
        self.cases.append(case)
        return case

    def evaluate(self):
        """Evaluate all test cases included in this test suite"""
        allTestsPassed = True
        for case in self.cases:
            case.evaluate()
            allTestsPassed = allTestsPassed and case.success
        self.success = allTestsPassed

    def getOrCreateTestCase(self, expressionToEvaluate):
        """Get a test case by expression, and create it if needed"""
        existingTestCase = self.getTestCaseByExpression(expressionToEvaluate)
        if (existingTestCase is not None):
            return existingTestCase
        return self.createTestCase(expressionToEvaluate)

    def getTestCaseByExpression(self, expression):
        """Get test case by expression to evaluate"""
        for case in self.cases:
            if (case.expressionToEvaluate == expression):
                return case
        return None

    def printResults(self):
        """Print the results of the test suite in the standard output"""
        if (self.success):
            print("✔️ {0}".format(self.name))
        else:
            print("❌ {0}".format(self.name))
        for case in self.cases:
            case.printResults("    ")        

    def run(self):
        """Run all test cases included in this test suite and print results"""
        self.evaluate()
        self.printResults()

    def setGlobalsDictionary(self, globals):
        """Set the dictionary containing the current scope's global variables"""
        self.globals = globals



class TestCase():
    """A test case"""

    def __init__(self, expressionToEvaluate):
        """Create a new test case"""
        self.expressionToEvaluate = expressionToEvaluate
        self.globals = globals()

    def evaluate(self):
        """Evaluate the expression to be tested"""
        try:
            assert eval(self.expressionToEvaluate, self.globals)
            self.success = True
        except AssertionError:
            self.success = False
            self.errorType = "AssertionError"
            self.errorMessage = "Invalid result"
        except Exception as e:        
            self.success = False
            self.errorType = type(e).__name__
            self.errorMessage = str(e)

    def printResults(self, indentation):
        """Print the results of the test in the standard output"""
        if (self.success):
            print("{0}✔️ {1}".format(indentation, self.expressionToEvaluate))
        else:
            print("{0}❌ {1}  =>  {2}: {3}".format(indentation, self.expressionToEvaluate, self.errorType, self.errorMessage))

    def run(self, indentation = ""):
        """Evaluate and print test results"""
        self.evaluate()
        self.printResults(indentation)

    def setGlobalsDictionary(self, globals):
        """Set the dictionary containing the current scope's global variables"""
        self.globals = globals
