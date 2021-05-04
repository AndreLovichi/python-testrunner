#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module introduce a basic test runner inspired from "mocha" output.
"""

__author__ = "Romain Andre-Lovichi"
__licence__ = "GPL"



class TestRunner:
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



class TestSuite:
    """A test suite is a group of related test cases"""

    def __init__(self, name):
        """Create a new test suite"""
        self.name = name
        self.cases = []

    def clear(self):
        """Remove all test cases"""
        self.cases = []

    def createErrorTestCase(self, expression, expectedErrorType, expectedErrorMessage):
        """Create a new error test case"""
        errorTestCase = ErrorTestCase(expression, expectedErrorType, expectedErrorMessage)
        errorTestCase.setGlobalsDictionary(self.globals)
        self.cases.append(errorTestCase)
        return errorTestCase

    def createTestCase(self, expressionOrLinesToEvaluate, description = ""):
        """Create a new test case"""
        isMultiline = isinstance(expressionOrLinesToEvaluate, list)
        if (isMultiline):
            return self.createMultilineTestCase(expressionOrLinesToEvaluate, description)
        else:
            return self.createSinglelineTestCase(expressionOrLinesToEvaluate, description)            

    def createMultilineTestCase(self, lines, description = ""):
        """Create a new multiline test case"""
        multilineCase = MultilineTestCase(lines, description)
        multilineCase.setGlobalsDictionary(self.globals)
        self.cases.append(multilineCase)
        return multilineCase

    def createSinglelineTestCase(self, expressionToEvaluate, description = ""):
        """Create a new singleline test case"""
        case = TestCase(expressionToEvaluate, description)
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

    def getOrCreateErrorTestCase(self, expression, expectedErrorType, expectedErrorMessage):
        """Get an error test case by expression, and create it if needed"""
        existingErrorTestCase = self.getErrorTestCaseByExpression(expression)
        if (existingErrorTestCase is not None):
            return existingErrorTestCase
        return self.createErrorTestCase(expression, expectedErrorType, expectedErrorMessage)

    def getOrCreateTestCase(self, expressionOrLinesToEvaluate, description = ""):
        """Get a test case by expression, and create it if needed"""
        existingTestCase = self.getTestCaseByExpression(expressionOrLinesToEvaluate)
        if (existingTestCase is not None):
            return existingTestCase
        return self.createTestCase(expressionOrLinesToEvaluate, description)

    def getErrorTestCaseByExpression(self, expression):
        for case in self.cases:
            if (hasattr(case, "expressionToEvaluate") and case.expressionToEvaluate == expression):
                return case
        return None        

    def getTestCaseByExpression(self, expressionOrLines):
        """Get test case by expression to evaluate or lines"""
        isMultiline = isinstance(expressionOrLines, list)
        if (isMultiline):
            return self.getMultilineTestCaseByLines(expressionOrLines)
        else:
            return self.getSinglelineTestCaseByExpression(expressionOrLines)

    def getMultilineTestCaseByLines(self, lines):
        """Get multiline test case by expression to evaluate"""
        for case in self.cases:
            if (hasattr(case, "lines") and case.lines == lines):
                return case
        return None

    def getSinglelineTestCaseByExpression(self, expression):
        """Get singleline test case by expression to evaluate"""
        for case in self.cases:
            if (hasattr(case, "expressionToEvaluate") and case.expressionToEvaluate == expression):
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



class TestCase:
    """A test case"""

    def __init__(self, expressionToEvaluate, description = ""):
        """Create a new test case"""
        self.expressionToEvaluate = expressionToEvaluate
        self.description = description if (description != "") else expressionToEvaluate
        self.globals = globals()

    def evaluate(self):
        """Evaluate the expression to be tested"""
        try:
            assertionErrorMessage = "The assertion \"{0}\" should be true".format(self.expressionToEvaluate)
            assert eval(self.expressionToEvaluate, self.globals), assertionErrorMessage
            self.markAsSuccess()
        except Exception as error:
            self.markAsFailed(error)

    def markAsFailed(self, error):
        """Mark this test case as error (and set all error-related fields)"""
        self.success = False
        self.errorType = type(error).__name__
        self.errorMessage = str(error)

    def markAsSuccess(self):
        """Mark this test case as success"""
        self.success = True

    def printResults(self, indentation):
        """Print the results of the test in the standard output"""
        if (self.success):
            print("{0}✔️ {1}".format(indentation, self.description))
        else:
            print("{0}❌ {1}  =>  {2}: {3}".format(indentation, self.description, self.errorType, self.errorMessage))

    def reset(self):
        attributesToDelete = ["errorMessage", "errorType", "success"]
        for attributeToDelete in attributesToDelete:
            if (hasattr(self, attributeToDelete)):
                delattr(self, attributeToDelete)

    def run(self, indentation = ""):
        """Evaluate and print test results"""
        self.reset()
        self.evaluate()
        self.printResults(indentation)

    def setGlobalsDictionary(self, globals):
        """Set the dictionary containing the current scope's global variables"""
        self.globals = globals



class ErrorTestCase(TestCase):
    """A test case that should raise an error"""

    def __init__(self, expressionToEvaluate, errorType, errorMessage = None, description = ""):
        """Create a new error test case"""
        TestCase.__init__(self, expressionToEvaluate, description)
        self.description = "{0} should raise a {1}".format(expressionToEvaluate, errorType)
        if (errorMessage is not None):
            self.description += " with message \"{0}\"".format(errorMessage)
        self.expectedErrorType = errorType
        self.expectedErrorMessage = errorMessage

    def markAsFailed(self):
        self.success = False
        self.errorType = "ExpectedError"
        if (self.actualErrorType is None):
            self.errorMessage = "No error was raised"
        else:
            self.errorMessage = "Raised instead a {0}".format(self.actualErrorType)
            if (self.actualErrorMessage is not None):
                self.errorMessage += " with message \"{0}\"".format(self.actualErrorMessage)

    def evaluate(self):
        self.actualErrorType = None
        self.actualErrorMessage = None
        try:
            eval(self.expressionToEvaluate, self.globals)
            self.markAsFailed()
        except Exception as error:
            self.actualErrorType = type(error).__name__
            self.actualErrorMessage = str(error)
            if (self.isExpectedError()):
                self.markAsSuccess()
            else:
                self.markAsFailed()
        
    def isExpectedError(self):
        if (self.actualErrorType != self.expectedErrorType):
            return False
        if (self.expectedErrorMessage is None):
            return True
        else:
            return self.actualErrorMessage == self.expectedErrorMessage



class MultilineTestCase(TestCase):
    """"A multiline test case"""

    def __init__(self, lines, description = ""):
        """Create a new multiline test case (only the last line will be evaluated)"""
        self.lines = lines
        lineToEvaluate = lines[len(lines) - 1]
        multilineDescription = description if (description != "") else " ; ".join(lines)         
        TestCase.__init__(self, lineToEvaluate, multilineDescription)

    def evaluate(self):
        """Evaluate the expression to be tested"""
        TestCase.reset(self)
        self.executeAllLinesExceptLast()
        if (hasattr(self, "success") and self.success == False):
            return
        TestCase.evaluate(self)

    def executeAllLinesExceptLast(self):
        """Execute all lines except the last one (to be evaluated separately)"""
        try:
            for i in range(len(self.lines) - 1):
                exec(self.lines[i], self.globals)
        except Exception as error:
            self.markAsFailed(error)