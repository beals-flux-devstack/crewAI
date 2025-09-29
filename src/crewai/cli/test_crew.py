"""
CLI command for running CrewAI testing framework.
"""

import os
import sys
from pathlib import Path

import click

from crewai.testing.runner import TestRunner


def test_crew_framework(
    test_dir: str = "tests",
    pattern: str = "test_*.py",
    verbosity: int = 2,
    report: bool = False,
    report_file: str = "crewai_test_report.html",
) -> None:
    """
    Run CrewAI testing framework.

    Args:
        test_dir: Directory containing test files
        pattern: Pattern for test file names
        verbosity: Output verbosity level
        report: Generate HTML report
        report_file: HTML report file path
    """
    try:
        # Initialize test runner
        runner = TestRunner(verbosity=verbosity)

        # Check if test directory exists
        if not os.path.exists(test_dir):
            click.echo(f"Test directory '{test_dir}' not found.")
            click.echo("To get started with CrewAI testing:")
            click.echo(f"1. Create a '{test_dir}' directory")
            click.echo("2. Add test files following the pattern 'test_*.py'")
            click.echo("3. Use AgentTestCase or CrewTestCase as base classes")
            return

        click.echo(f"Discovering CrewAI tests in '{test_dir}' with pattern '{pattern}'...")

        # Discover tests
        test_suite = runner.discover_crewai_tests(test_dir=test_dir)

        # Check if any tests were found
        if test_suite.countTestCases() == 0:
            click.echo("No CrewAI tests found.")
            click.echo("Make sure your test files:")
            click.echo("- Start with 'test_' and end with '.py'")
            click.echo("- Contain classes inheriting from AgentTestCase or CrewTestCase")
            click.echo("- Have test methods starting with 'test_'")
            return

        click.echo(f"Found {test_suite.countTestCases()} test(s)")
        click.echo("Running tests...")

        # Run tests
        result = runner.run_tests(test_suite)

        # Print results
        runner.print_results(result)

        # Generate report if requested
        if report:
            runner.generate_report(result, report_file)

        # Exit with error code if tests failed
        if result.failures or result.errors:
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error running tests: {e}")
        sys.exit(1)