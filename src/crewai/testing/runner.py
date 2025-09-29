"""
Test Runner for CrewAI Testing Framework.

Provides test discovery, execution, and reporting capabilities
specifically designed for CrewAI applications.
"""

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from typing import Any, Type

from crewai.testing.agent_test_case import AgentTestCase
from crewai.testing.crew_test_case import CrewTestCase


class CrewAITestResult(unittest.TestResult):
    """
    Custom test result class for CrewAI testing.

    Provides enhanced reporting and metrics specific to agent and crew testing.
    """

    def __init__(self) -> None:
        super().__init__()
        self.agent_test_results: list[dict[str, Any]] = []
        self.crew_test_results: list[dict[str, Any]] = []
        self.performance_metrics: dict[str, Any] = {}

    def addSuccess(self, test: unittest.TestCase) -> None:
        """Record a successful test."""
        super().addSuccess(test)
        self._record_test_result(test, 'success')

    def addError(self, test: unittest.TestCase, err: Any) -> None:
        """Record a test error."""
        super().addError(test, err)
        self._record_test_result(test, 'error', err)

    def addFailure(self, test: unittest.TestCase, err: Any) -> None:
        """Record a test failure."""
        super().addFailure(test, err)
        self._record_test_result(test, 'failure', err)

    def _record_test_result(
        self,
        test: unittest.TestCase,
        status: str,
        error_info: Any = None,
    ) -> None:
        """Record detailed test result information."""
        test_info = {
            'test_name': test._testMethodName,
            'test_class': test.__class__.__name__,
            'status': status,
            'error_info': error_info,
        }

        if isinstance(test, AgentTestCase):
            self.agent_test_results.append(test_info)
        elif isinstance(test, CrewTestCase):
            self.crew_test_results.append(test_info)

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of test results."""
        return {
            'total_tests': self.testsRun,
            'successes': self.testsRun - len(self.failures) - len(self.errors),
            'failures': len(self.failures),
            'errors': len(self.errors),
            'agent_tests': len(self.agent_test_results),
            'crew_tests': len(self.crew_test_results),
            'success_rate': self._calculate_success_rate(),
        }

    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate."""
        if self.testsRun == 0:
            return 0.0
        return (self.testsRun - len(self.failures) - len(self.errors)) / self.testsRun


class TestRunner:
    """
    Main test runner for CrewAI testing framework.

    Provides test discovery, execution, and reporting capabilities.
    """

    def __init__(self, verbosity: int = 2):
        """
        Initialize the test runner.

        Args:
            verbosity: Test output verbosity level (0-2)
        """
        self.verbosity = verbosity
        self.test_suite: unittest.TestSuite | None = None

    def discover_tests(
        self,
        start_dir: str = ".",
        pattern: str = "test_*.py",
        top_level_dir: str | None = None,
    ) -> unittest.TestSuite:
        """
        Discover test files and create test suite.

        Args:
            start_dir: Directory to start test discovery
            pattern: Pattern for test file names
            top_level_dir: Top-level directory for imports

        Returns:
            unittest.TestSuite: Discovered test suite
        """
        loader = unittest.TestLoader()

        # Use unittest's discovery mechanism
        suite = loader.discover(
            start_dir=start_dir,
            pattern=pattern,
            top_level_dir=top_level_dir,
        )

        self.test_suite = suite
        return suite

    def discover_crewai_tests(
        self,
        test_dir: str = "tests",
    ) -> unittest.TestSuite:
        """
        Discover CrewAI-specific tests.

        Args:
            test_dir: Directory containing test files

        Returns:
            unittest.TestSuite: Test suite with CrewAI tests
        """
        suite = unittest.TestSuite()

        if not os.path.exists(test_dir):
            return suite

        for root, dirs, files in os.walk(test_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    module_path = os.path.join(root, file)
                    module = self._load_module_from_path(module_path)

                    if module:
                        # Find CrewAI test classes
                        for name in dir(module):
                            obj = getattr(module, name)
                            if (isinstance(obj, type) and
                                issubclass(obj, (AgentTestCase, CrewTestCase)) and
                                obj not in (AgentTestCase, CrewTestCase)):

                                # Add all test methods from this class
                                for method_name in dir(obj):
                                    if method_name.startswith('test_'):
                                        suite.addTest(obj(method_name))

        self.test_suite = suite
        return suite

    def run_tests(
        self,
        test_suite: unittest.TestSuite | None = None,
    ) -> CrewAITestResult:
        """
        Run the test suite.

        Args:
            test_suite: Test suite to run (uses discovered if not provided)

        Returns:
            CrewAITestResult: Test execution results
        """
        suite = test_suite or self.test_suite
        if suite is None:
            raise ValueError("No test suite available. Run discover_tests() first.")

        # Create custom test result
        result = CrewAITestResult()

        # Run the tests
        suite.run(result)

        return result

    def run_single_test(
        self,
        test_class: Type[unittest.TestCase],
        test_method: str,
    ) -> CrewAITestResult:
        """
        Run a single test method.

        Args:
            test_class: Test class to run
            test_method: Test method name

        Returns:
            CrewAITestResult: Test execution results
        """
        suite = unittest.TestSuite()
        suite.addTest(test_class(test_method))

        return self.run_tests(suite)

    def print_results(self, result: CrewAITestResult) -> None:
        """
        Print test results to console.

        Args:
            result: Test results to print
        """
        summary = result.get_summary()

        print("\n" + "="*60)
        print("CrewAI Test Results Summary")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successes: {summary['successes']}")
        print(f"Failures: {summary['failures']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Agent Tests: {summary['agent_tests']}")
        print(f"Crew Tests: {summary['crew_tests']}")

        if result.failures:
            print(f"\nFailures ({len(result.failures)}):")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")

        if result.errors:
            print(f"\nErrors ({len(result.errors)}):")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")

        print("="*60)

    def _load_module_from_path(self, path: str) -> Any:
        """
        Load a Python module from file path.

        Args:
            path: Path to Python file

        Returns:
            Any: Loaded module or None if failed
        """
        try:
            module_name = os.path.splitext(os.path.basename(path))[0]
            spec = importlib.util.spec_from_file_location(module_name, path)

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                return module

        except Exception as e:
            print(f"Warning: Failed to load module from {path}: {e}")

        return None

    def generate_report(
        self,
        result: CrewAITestResult,
        output_file: str = "crewai_test_report.html",
    ) -> None:
        """
        Generate HTML test report.

        Args:
            result: Test results
            output_file: Output file path
        """
        summary = result.get_summary()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CrewAI Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .success {{ color: green; }}
                .failure {{ color: red; }}
                .error {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>CrewAI Test Report</h1>

            <div class="summary">
                <h2>Summary</h2>
                <p>Total Tests: {summary['total_tests']}</p>
                <p class="success">Successes: {summary['successes']}</p>
                <p class="failure">Failures: {summary['failures']}</p>
                <p class="error">Errors: {summary['errors']}</p>
                <p>Success Rate: {summary['success_rate']:.1%}</p>
                <p>Agent Tests: {summary['agent_tests']}</p>
                <p>Crew Tests: {summary['crew_tests']}</p>
            </div>

            <!-- Additional detailed results would go here -->

        </body>
        </html>
        """

        with open(output_file, 'w') as f:
            f.write(html_content)

        print(f"Report generated: {output_file}")