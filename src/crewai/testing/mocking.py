"""
Mocking utilities for CrewAI testing framework.

Provides mock implementations of agents and tools for isolated testing,
allowing developers to test components without external dependencies.
"""

from typing import Any, Callable
from unittest.mock import MagicMock, Mock

from crewai.agent import Agent
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.task import Task
from crewai.tasks.task_output import TaskOutput
from crewai.tools.base_tool import BaseTool


class MockAgent(BaseAgent):
    """
    Mock agent for testing purposes.

    Allows controlled responses and behavior for isolated testing
    without invoking actual LLM calls or complex agent logic.
    """

    def __init__(
        self,
        role: str = "Mock Agent",
        goal: str = "Provide mock responses",
        backstory: str = "A mock agent for testing",
        responses: list[str] | None = None,
        **kwargs: Any,
    ):
        """
        Initialize mock agent.

        Args:
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            responses: Predefined responses to return in sequence
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.responses = responses or ["Mock response"]
        self.response_index = 0
        self.execution_history: list[dict[str, Any]] = []
        self.tool_calls: list[dict[str, Any]] = []

    def execute_task(self, task: Task) -> TaskOutput:
        """
        Execute a task and return a mock response.

        Args:
            task: Task to execute

        Returns:
            TaskOutput: Mock task output
        """
        # Get next response
        response = self.get_next_response()

        # Record execution
        execution_record = {
            'task_description': task.description,
            'response': response,
            'timestamp': self._get_current_timestamp(),
        }
        self.execution_history.append(execution_record)

        # Create mock task output
        task_output = TaskOutput(
            description=task.description,
            raw=response,
            agent=self.role,
        )

        return task_output

    def get_next_response(self) -> str:
        """Get the next predefined response."""
        if not self.responses:
            return "Mock response"

        response = self.responses[self.response_index % len(self.responses)]
        self.response_index += 1
        return response

    def add_response(self, response: str) -> None:
        """Add a response to the queue."""
        self.responses.append(response)

    def set_responses(self, responses: list[str]) -> None:
        """Set new response queue."""
        self.responses = responses
        self.response_index = 0

    def simulate_tool_call(
        self,
        tool_name: str,
        parameters: dict[str, Any],
        result: Any = "Mock tool result",
    ) -> None:
        """
        Simulate a tool call for testing tool usage patterns.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters
            result: Simulated tool result
        """
        tool_call = {
            'tool_name': tool_name,
            'parameters': parameters,
            'result': result,
            'timestamp': self._get_current_timestamp(),
        }
        self.tool_calls.append(tool_call)

    def get_execution_history(self) -> list[dict[str, Any]]:
        """Get the agent's execution history."""
        return self.execution_history.copy()

    def get_tool_calls(self) -> list[dict[str, Any]]:
        """Get the agent's tool call history."""
        return self.tool_calls.copy()

    def reset_history(self) -> None:
        """Reset execution and tool call history."""
        self.execution_history.clear()
        self.tool_calls.clear()
        self.response_index = 0

    def _get_current_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()


class MockTool(BaseTool):
    """
    Mock tool for testing purposes.

    Provides controlled tool behavior for testing agent tool usage
    without external dependencies.
    """

    def __init__(
        self,
        name: str = "mock_tool",
        description: str = "A mock tool for testing",
        return_value: Any = "Mock tool result",
        side_effect: Callable[..., Any] | None = None,
        **kwargs: Any,
    ):
        """
        Initialize mock tool.

        Args:
            name: Tool name
            description: Tool description
            return_value: Value to return when called
            side_effect: Function to call instead of returning value
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.return_value = return_value
        self.side_effect = side_effect
        self.call_history: list[dict[str, Any]] = []

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the mock tool.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Any: Mock result
        """
        # Record the call
        call_record = {
            'args': args,
            'kwargs': kwargs,
            'timestamp': self._get_current_timestamp(),
        }
        self.call_history.append(call_record)

        # Return result
        if self.side_effect:
            return self.side_effect(*args, **kwargs)
        return self.return_value

    def get_call_history(self) -> list[dict[str, Any]]:
        """Get the tool's call history."""
        return self.call_history.copy()

    def reset_history(self) -> None:
        """Reset call history."""
        self.call_history.clear()

    def was_called(self) -> bool:
        """Check if the tool was called."""
        return len(self.call_history) > 0

    def was_called_with(self, *args: Any, **kwargs: Any) -> bool:
        """Check if tool was called with specific arguments."""
        for call in self.call_history:
            if call['args'] == args and call['kwargs'] == kwargs:
                return True
        return False

    def call_count(self) -> int:
        """Get the number of times the tool was called."""
        return len(self.call_history)

    def _get_current_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()


def create_mock_agent_with_tools(
    agent_config: dict[str, Any],
    tool_configs: list[dict[str, Any]],
) -> tuple[MockAgent, list[MockTool]]:
    """
    Create a mock agent with mock tools.

    Args:
        agent_config: Configuration for the mock agent
        tool_configs: List of configurations for mock tools

    Returns:
        tuple: Mock agent and list of mock tools
    """
    # Create mock tools
    mock_tools = []
    for tool_config in tool_configs:
        mock_tool = MockTool(**tool_config)
        mock_tools.append(mock_tool)

    # Create mock agent with tools
    agent_config['tools'] = mock_tools
    mock_agent = MockAgent(**agent_config)

    return mock_agent, mock_tools


def patch_agent_llm(agent: Agent | BaseAgent, mock_responses: list[str]) -> Mock:
    """
    Patch an agent's LLM to return mock responses.

    Args:
        agent: Agent to patch
        mock_responses: List of responses to return

    Returns:
        Mock: The mock LLM object
    """
    mock_llm = MagicMock()
    mock_llm.call.side_effect = mock_responses

    # Patch the agent's LLM
    if hasattr(agent, 'llm'):
        agent.llm = mock_llm
    elif hasattr(agent, '_llm'):
        agent._llm = mock_llm

    return mock_llm


def patch_crew_agents(crew: Any, mock_agents: list[MockAgent]) -> None:
    """
    Replace crew agents with mock agents for testing.

    Args:
        crew: Crew to patch
        mock_agents: List of mock agents to use
    """
    crew.agents = mock_agents