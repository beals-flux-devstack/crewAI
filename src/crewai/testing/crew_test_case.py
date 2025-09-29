"""
Crew Test Case - Integration testing framework for CrewAI crews.

Provides a base class and utilities for testing crew workflows, agent collaboration,
and end-to-end execution scenarios.
"""

import unittest
from typing import Any

from crewai.agent import Agent
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.crew import Crew
from crewai.crews.crew_output import CrewOutput
from crewai.process import Process
from crewai.task import Task
from crewai.testing.assertions import (
    assert_crew_completed_successfully,
    assert_crew_output_matches,
    assert_output_format,
)


class CrewTestCase(unittest.TestCase):
    """
    Base test case class for testing crew workflows and integration.

    Provides utilities and setup methods for testing multi-agent collaboration,
    task execution workflows, and crew-level behavior.
    """

    def setUp(self) -> None:
        """Set up test environment before each test method."""
        super().setUp()
        self.crew: Crew | None = None
        self.test_agents: list[Agent | BaseAgent] = []
        self.test_tasks: list[Task] = []
        self.crew_outputs: list[CrewOutput] = []

    def tearDown(self) -> None:
        """Clean up test environment after each test method."""
        super().tearDown()
        self.crew = None
        self.test_agents.clear()
        self.test_tasks.clear()
        self.crew_outputs.clear()

    def create_test_crew(
        self,
        agents: list[Agent | BaseAgent] | None = None,
        tasks: list[Task] | None = None,
        process: Process = Process.sequential,
        verbose: bool = False,
        **kwargs: Any,
    ) -> Crew:
        """
        Create a test crew with specified configuration.

        Args:
            agents: List of agents for the crew
            tasks: List of tasks for the crew
            process: Execution process (sequential, hierarchical)
            verbose: Whether to enable verbose output
            **kwargs: Additional crew configuration

        Returns:
            Crew: Configured test crew
        """
        crew_agents = agents or self.test_agents
        crew_tasks = tasks or self.test_tasks

        if not crew_agents:
            raise ValueError("No agents available. Create agents first or pass them explicitly.")

        if not crew_tasks:
            raise ValueError("No tasks available. Create tasks first or pass them explicitly.")

        self.crew = Crew(
            agents=crew_agents,
            tasks=crew_tasks,
            process=process,
            verbose=verbose,
            **kwargs
        )
        return self.crew

    def add_test_agent(
        self,
        role: str,
        goal: str,
        backstory: str,
        **kwargs: Any,
    ) -> Agent:
        """
        Create and add a test agent to the crew.

        Args:
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            **kwargs: Additional agent configuration

        Returns:
            Agent: Created and added agent
        """
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=kwargs.get('verbose', False),
            **kwargs
        )
        self.test_agents.append(agent)
        return agent

    def add_test_task(
        self,
        description: str,
        expected_output: str | None = None,
        agent: Agent | BaseAgent | None = None,
        **kwargs: Any,
    ) -> Task:
        """
        Create and add a test task to the crew.

        Args:
            description: Task description
            expected_output: Expected task output
            agent: Agent to assign to task
            **kwargs: Additional task configuration

        Returns:
            Task: Created and added task
        """
        if agent is None and self.test_agents:
            agent = self.test_agents[0]  # Default to first agent

        task = Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            **kwargs
        )
        self.test_tasks.append(task)
        return task

    def execute_crew(
        self,
        inputs: dict[str, Any] | None = None,
        crew: Crew | None = None,
    ) -> CrewOutput:
        """
        Execute a crew and capture the output.

        Args:
            inputs: Input data for the crew execution
            crew: Crew to execute (defaults to self.crew)

        Returns:
            CrewOutput: The crew execution result
        """
        executing_crew = crew or self.crew
        if executing_crew is None:
            raise ValueError("No crew available for execution. Create a crew first.")

        # Execute the crew
        output = executing_crew.kickoff(inputs=inputs or {})
        self.crew_outputs.append(output)
        return output

    def create_collaborative_scenario(
        self,
        scenario_name: str,
        agent_configs: list[dict[str, Any]],
        task_configs: list[dict[str, Any]],
    ) -> tuple[list[Agent], list[Task]]:
        """
        Create a predefined collaborative scenario for testing.

        Args:
            scenario_name: Name of the scenario
            agent_configs: List of agent configuration dictionaries
            task_configs: List of task configuration dictionaries

        Returns:
            tuple: Created agents and tasks
        """
        agents = []
        tasks = []

        # Create agents
        for config in agent_configs:
            agent = self.add_test_agent(**config)
            agents.append(agent)

        # Create tasks
        for i, config in enumerate(task_configs):
            # Assign agent if not specified
            if 'agent' not in config and agents:
                config['agent'] = agents[i % len(agents)]

            task = self.add_test_task(**config)
            tasks.append(task)

        return agents, tasks

    # Convenience assertion methods

    def assertCrewCompletedSuccessfully(
        self,
        crew_output: CrewOutput,
        msg: str | None = None,
    ) -> None:
        """Assert that crew execution completed successfully."""
        assert_crew_completed_successfully(crew_output, msg)

    def assertCrewOutputMatches(
        self,
        crew_output: CrewOutput,
        expected_pattern: str,
        regex: bool = False,
        msg: str | None = None,
    ) -> None:
        """Assert that crew output matches expected pattern."""
        assert_crew_output_matches(crew_output, expected_pattern, regex, msg)

    def assertCrewOutputFormat(
        self,
        crew_output: CrewOutput,
        format_type: str,
        msg: str | None = None,
    ) -> None:
        """Assert that crew output matches expected format."""
        assert_output_format(crew_output, format_type, msg)

    def assertAgentCollaboration(
        self,
        crew_output: CrewOutput,
        min_agent_interactions: int = 2,
        msg: str | None = None,
    ) -> None:
        """
        Assert that agents collaborated during crew execution.

        Args:
            crew_output: Crew execution output
            min_agent_interactions: Minimum number of agent interactions expected
            msg: Optional custom error message
        """
        # This would need to be implemented with proper interaction tracking
        # For now, it's a placeholder for the interface
        pass

    def assertTaskSequence(
        self,
        crew_output: CrewOutput,
        expected_sequence: list[str],
        msg: str | None = None,
    ) -> None:
        """
        Assert that tasks were executed in expected sequence.

        Args:
            crew_output: Crew execution output
            expected_sequence: List of task descriptions in expected order
            msg: Optional custom error message
        """
        # This would need proper task execution tracking
        # For now, it's a placeholder for the interface
        pass

    def get_last_crew_output(self) -> CrewOutput | None:
        """Get the most recent crew output from test execution."""
        return self.crew_outputs[-1] if self.crew_outputs else None

    def get_crew_task_outputs(self, crew_output: CrewOutput | None = None) -> list[Any]:
        """Get individual task outputs from crew execution."""
        output = crew_output or self.get_last_crew_output()
        if output is None:
            return []

        return output.tasks_output if hasattr(output, 'tasks_output') else []

    def measure_crew_performance(
        self,
        crew_output: CrewOutput,
    ) -> dict[str, Any]:
        """
        Measure crew performance metrics.

        Args:
            crew_output: Crew execution output

        Returns:
            dict: Performance metrics
        """
        # This would include actual performance measurement
        # For now, it's a placeholder structure
        return {
            'execution_time': 0.0,
            'total_tasks': len(self.test_tasks),
            'successful_tasks': len(self.get_crew_task_outputs(crew_output)),
            'agent_utilization': {},
            'collaboration_score': 0.0,
        }