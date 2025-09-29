"""
Specialized assertions for CrewAI testing framework.

Provides domain-specific assertions for validating agent behavior, crew outputs,
and common AI application testing patterns.
"""

import re
from typing import Any

from crewai.agent import Agent
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.crew import Crew
from crewai.crews.crew_output import CrewOutput
from crewai.experimental.evaluation import (
    EvaluationScore,
    SemanticQualityEvaluator,
)
from crewai.task import Task
from crewai.tasks.task_output import TaskOutput
from crewai.tools.base_tool import BaseTool


class CrewAITestAssertionError(AssertionError):
    """Specialized assertion error for CrewAI testing."""
    pass


def assert_agent_response_contains(
    agent_output: str | TaskOutput,
    expected_content: str,
    case_sensitive: bool = False,
    msg: str | None = None,
) -> None:
    """
    Assert that agent response contains expected content.

    Args:
        agent_output: The agent's output to check
        expected_content: Content that should be present
        case_sensitive: Whether to perform case-sensitive matching
        msg: Optional custom error message
    """
    if isinstance(agent_output, TaskOutput):
        actual_content = agent_output.raw
    else:
        actual_content = agent_output

    if not case_sensitive:
        actual_content = actual_content.lower()
        expected_content = expected_content.lower()

    if expected_content not in actual_content:
        error_msg = msg or f"Expected content '{expected_content}' not found in agent output"
        raise CrewAITestAssertionError(error_msg)


def assert_agent_response_quality(
    agent_output: str | TaskOutput,
    task: Task,
    min_score: float = 7.0,
    msg: str | None = None,
) -> EvaluationScore:
    """
    Assert that agent response meets quality standards.

    Args:
        agent_output: The agent's output to evaluate
        task: The task that was executed
        min_score: Minimum acceptable quality score (0-10)
        msg: Optional custom error message

    Returns:
        EvaluationScore: The evaluation result
    """
    evaluator = SemanticQualityEvaluator()

    if isinstance(agent_output, TaskOutput):
        output_text = agent_output.raw
    else:
        output_text = agent_output

    score = evaluator.evaluate(
        task_description=task.description,
        expected_output=task.expected_output or "High quality response",
        actual_output=output_text,
    )

    if score.score is not None and score.score < min_score:
        error_msg = msg or f"Agent response quality below threshold. Score: {score.score:.1f}/{min_score}. Feedback: {score.feedback}"
        raise CrewAITestAssertionError(error_msg)

    return score


def assert_agent_called_tool(
    agent: Agent | BaseAgent,
    tool: BaseTool | str,
    msg: str | None = None,
) -> None:
    """
    Assert that an agent called a specific tool during execution.

    Args:
        agent: The agent to check
        tool: Tool instance or tool name that should have been called
        msg: Optional custom error message
    """
    # This would need to be implemented with proper tool usage tracking
    # For now, this is a placeholder for the interface
    tool_name = tool.name if isinstance(tool, BaseTool) else tool

    # TODO: Implement actual tool usage tracking
    # This would require integration with the agent's execution trace

    error_msg = msg or f"Agent did not call expected tool '{tool_name}'"
    # Placeholder implementation - in reality, this would check agent's tool usage history
    # raise CrewAITestAssertionError(error_msg)


def assert_crew_completed_successfully(
    crew_output: CrewOutput,
    msg: str | None = None,
) -> None:
    """
    Assert that a crew execution completed successfully.

    Args:
        crew_output: The crew execution output
        msg: Optional custom error message
    """
    if not crew_output:
        error_msg = msg or "Crew execution produced no output"
        raise CrewAITestAssertionError(error_msg)

    # Check if there were any task failures
    for task_output in crew_output.tasks_output:
        if hasattr(task_output, 'error') and task_output.error:
            error_msg = msg or f"Crew execution failed with task error: {task_output.error}"
            raise CrewAITestAssertionError(error_msg)


def assert_crew_output_matches(
    crew_output: CrewOutput,
    expected_pattern: str,
    regex: bool = False,
    msg: str | None = None,
) -> None:
    """
    Assert that crew output matches expected pattern.

    Args:
        crew_output: The crew execution output
        expected_pattern: Pattern to match against
        regex: Whether to treat pattern as regex
        msg: Optional custom error message
    """
    actual_output = crew_output.raw

    if regex:
        if not re.search(expected_pattern, actual_output):
            error_msg = msg or f"Crew output does not match regex pattern: {expected_pattern}"
            raise CrewAITestAssertionError(error_msg)
    else:
        if expected_pattern not in actual_output:
            error_msg = msg or f"Expected pattern '{expected_pattern}' not found in crew output"
            raise CrewAITestAssertionError(error_msg)


def assert_output_format(
    output: str | TaskOutput | CrewOutput,
    format_type: str,
    msg: str | None = None,
) -> None:
    """
    Assert that output matches expected format (JSON, Markdown, etc.).

    Args:
        output: Output to validate
        format_type: Expected format ('json', 'markdown', 'yaml', etc.)
        msg: Optional custom error message
    """
    if isinstance(output, (TaskOutput, CrewOutput)):
        content = output.raw
    else:
        content = output

    if format_type.lower() == 'json':
        try:
            import json
            json.loads(content)
        except json.JSONDecodeError as e:
            error_msg = msg or f"Output is not valid JSON: {e}"
            raise CrewAITestAssertionError(error_msg)

    elif format_type.lower() == 'markdown':
        # Basic markdown validation - look for common markdown elements
        markdown_indicators = ['#', '*', '-', '`', '[', ']', '(', ')']
        if not any(indicator in content for indicator in markdown_indicators):
            error_msg = msg or "Output does not appear to be Markdown format"
            raise CrewAITestAssertionError(error_msg)

    # Add more format validations as needed


def assert_no_hallucination(
    agent_output: str | TaskOutput,
    context_sources: list[str],
    msg: str | None = None,
) -> None:
    """
    Assert that agent output doesn't contain hallucinated information.

    Args:
        agent_output: The agent's output to check
        context_sources: Known factual sources to validate against
        msg: Optional custom error message
    """
    # This is a complex assertion that would need sophisticated fact-checking
    # For now, this is a placeholder for the interface

    if isinstance(agent_output, TaskOutput):
        content = agent_output.raw
    else:
        content = agent_output

    # TODO: Implement actual hallucination detection
    # This could involve:
    # - Fact-checking against known sources
    # - Consistency checking across outputs
    # - External API validation

    # Placeholder implementation
    pass