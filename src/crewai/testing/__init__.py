"""
CrewAI Testing Framework

A comprehensive testing framework for CrewAI applications, providing utilities
for testing agent behavior, crew workflows, and output quality validation.

Core Components:
- AgentTestCase: Unit testing for individual agents
- CrewTestCase: Integration testing for crew workflows
- TestRunner: Test discovery and execution engine
- Assertions: Specialized assertions for agent/crew behavior
- Mocking: Mock agents and tools for isolated testing
"""

from crewai.testing.agent_test_case import AgentTestCase
from crewai.testing.assertions import (
    assert_agent_called_tool,
    assert_agent_response_contains,
    assert_agent_response_quality,
    assert_crew_completed_successfully,
    assert_crew_output_matches,
    assert_no_hallucination,
    assert_output_format,
)
from crewai.testing.crew_test_case import CrewTestCase
from crewai.testing.mocking import MockAgent, MockTool
from crewai.testing.runner import TestRunner

__all__ = [
    # Test Cases
    "AgentTestCase",
    "CrewTestCase",

    # Test Runner
    "TestRunner",

    # Assertions
    "assert_agent_called_tool",
    "assert_agent_response_contains",
    "assert_agent_response_quality",
    "assert_crew_completed_successfully",
    "assert_crew_output_matches",
    "assert_no_hallucination",
    "assert_output_format",

    # Mocking
    "MockAgent",
    "MockTool",
]