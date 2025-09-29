"""
Agent Test Case - Unit testing framework for individual CrewAI agents.

Provides a base class and utilities for testing agent behavior, responses,
and tool usage in isolation.
"""

import unittest
from typing import Any

from crewai.agent import Agent
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.task import Task
from crewai.tasks.task_output import TaskOutput
from crewai.testing.assertions import (
    assert_agent_response_contains,
    assert_agent_response_quality,
    assert_output_format,
)


class AgentTestCase(unittest.TestCase):
    """
    Base test case class for testing individual agents.

    Provides utilities and setup methods for testing agent behavior,
    responses, and tool usage patterns.
    """

    def setUp(self) -> None:
        """Set up test environment before each test method."""
        super().setUp()
        self.agent: Agent | BaseAgent | None = None
        self.test_tasks: list[Task] = []
        self.agent_outputs: list[TaskOutput] = []

    def tearDown(self) -> None:
        """Clean up test environment after each test method."""
        super().tearDown()
        self.agent = None
        self.test_tasks.clear()
        self.agent_outputs.clear()

    def create_test_agent(
        self,
        role: str = "Test Agent",
        goal: str = "Perform testing tasks effectively",
        backstory: str = "A specialized agent created for testing purposes",
        **kwargs: Any,
    ) -> Agent:
        """
        Create a test agent with default configuration.

        Args:
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            **kwargs: Additional agent configuration

        Returns:
            Agent: Configured test agent
        """
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=kwargs.get('verbose', False),
            **kwargs
        )
        return self.agent

    def create_test_task(
        self,
        description: str,
        expected_output: str | None = None,
        agent: Agent | BaseAgent | None = None,
        **kwargs: Any,
    ) -> Task:
        """
        Create a test task for agent execution.

        Args:
            description: Task description
            expected_output: Expected task output
            agent: Agent to assign to task (defaults to self.agent)
            **kwargs: Additional task configuration

        Returns:
            Task: Configured test task
        """
        task_agent = agent or self.agent
        if task_agent is None:
            raise ValueError("No agent available. Create an agent first or pass one explicitly.")

        task = Task(
            description=description,
            expected_output=expected_output,
            agent=task_agent,
            **kwargs
        )
        self.test_tasks.append(task)
        return task

    def execute_agent_task(
        self,
        task: Task,
        agent: Agent | BaseAgent | None = None,
    ) -> TaskOutput:
        """
        Execute a task with an agent and capture the output.

        Args:
            task: Task to execute
            agent: Agent to use (defaults to task's agent)

        Returns:
            TaskOutput: The task execution result
        """
        executing_agent = agent or task.agent
        if executing_agent is None:
            raise ValueError("No agent available for task execution.")

        # Execute the task - this would be the actual execution
        # For now, we'll create a placeholder output
        # In reality, this would call the agent's execute method
        output = executing_agent.execute_task(task)
        self.agent_outputs.append(output)
        return output

    # Convenience assertion methods that wrap the module-level assertions

    def assertAgentResponseContains(
        self,
        agent_output: str | TaskOutput,
        expected_content: str,
        case_sensitive: bool = False,
        msg: str | None = None,
    ) -> None:
        """Assert that agent response contains expected content."""
        assert_agent_response_contains(
            agent_output, expected_content, case_sensitive, msg
        )

    def assertAgentResponseQuality(
        self,
        agent_output: str | TaskOutput,
        task: Task,
        min_score: float = 7.0,
        msg: str | None = None,
    ) -> None:
        """Assert that agent response meets quality standards."""
        assert_agent_response_quality(agent_output, task, min_score, msg)

    def assertOutputFormat(
        self,
        output: str | TaskOutput,
        format_type: str,
        msg: str | None = None,
    ) -> None:
        """Assert that output matches expected format."""
        assert_output_format(output, format_type, msg)

    def assertAgentUsedTool(
        self,
        tool_name: str,
        agent: Agent | BaseAgent | None = None,
        msg: str | None = None,
    ) -> None:
        """Assert that agent used a specific tool."""
        test_agent = agent or self.agent
        if test_agent is None:
            raise ValueError("No agent available to check tool usage.")

        # This would need proper tool usage tracking implementation
        # For now, it's a placeholder
        pass

    def get_last_agent_output(self) -> TaskOutput | None:
        """Get the most recent agent output from test execution."""
        return self.agent_outputs[-1] if self.agent_outputs else None

    def get_agent_outputs_containing(self, content: str) -> list[TaskOutput]:
        """Get all agent outputs that contain specific content."""
        return [
            output for output in self.agent_outputs
            if content.lower() in output.raw.lower()
        ]