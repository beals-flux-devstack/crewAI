# CrewAI Testing Framework

A comprehensive testing framework for CrewAI applications, providing utilities for testing agent behavior, crew workflows, and output quality validation.

## Overview

The CrewAI Testing Framework extends the existing evaluation system to provide production-ready testing capabilities for multi-agent systems. It includes:

- **Agent Testing**: Unit tests for individual agent behavior
- **Crew Testing**: Integration tests for multi-agent workflows
- **Quality Assurance**: Output quality validation and format checking
- **Mock Utilities**: Mock agents and tools for isolated testing
- **CLI Integration**: Command-line test runner with reporting

## Quick Start

### Installation

The testing framework is included with CrewAI. No additional installation required.

### Basic Usage

```python
from crewai import Agent, Task
from crewai.testing import AgentTestCase

class TestMyAgent(AgentTestCase):
    def setUp(self):
        self.create_test_agent(
            role="Research Assistant",
            goal="Provide accurate research insights",
            backstory="Experienced researcher with analytical skills"
        )

    def test_agent_research_capability(self):
        task = self.create_test_task(
            description="Research AI trends in 2024",
            expected_output="Comprehensive analysis of AI trends"
        )

        # In practice, you would execute the task
        # output = self.execute_agent_task(task)

        # For demonstration, using mock output
        mock_output = "AI trends include multimodal systems..."

        self.assertAgentResponseContains(mock_output, "AI trends")
        self.assertOutputFormat(mock_output, "text")
```

### Running Tests

```bash
# Run all tests in tests/ directory
crewai test-framework

# Run tests with custom options
crewai test-framework -d my_tests -p "test_*.py" --report

# Generate HTML report
crewai test-framework --report --report-file custom_report.html
```

## Core Components

### 1. AgentTestCase

Base class for testing individual agents in isolation.

```python
from crewai.testing import AgentTestCase

class TestResearchAgent(AgentTestCase):
    def setUp(self):
        # Create test agent
        self.create_test_agent(
            role="Senior Researcher",
            goal="Conduct thorough research",
            backstory="Expert researcher with 10+ years experience"
        )

    def test_agent_provides_insights(self):
        task = self.create_test_task(
            description="Analyze market trends",
            expected_output="Market analysis with insights"
        )

        # Test execution would happen here
        # output = self.execute_agent_task(task)

        # Assertions
        # self.assertAgentResponseQuality(output, task, min_score=7.0)
        # self.assertAgentResponseContains(output, "market trends")
```

**Key Methods:**
- `create_test_agent()`: Create agent for testing
- `create_test_task()`: Create task for agent execution
- `execute_agent_task()`: Execute task with agent
- `assertAgentResponseContains()`: Check response content
- `assertAgentResponseQuality()`: Validate response quality
- `assertOutputFormat()`: Verify output format

### 2. CrewTestCase

Base class for testing crew workflows and collaboration.

```python
from crewai.testing import CrewTestCase
from crewai import Process

class TestContentCrew(CrewTestCase):
    def setUp(self):
        # Add agents to crew
        self.add_test_agent(
            role="Researcher",
            goal="Gather information",
            backstory="Research specialist"
        )
        self.add_test_agent(
            role="Writer",
            goal="Create content",
            backstory="Skilled content writer"
        )

    def test_content_workflow(self):
        # Add tasks
        self.add_test_task(
            description="Research topic X",
            expected_output="Research summary"
        )
        self.add_test_task(
            description="Write article based on research",
            expected_output="Well-written article"
        )

        # Create crew
        crew = self.create_test_crew(
            process=Process.sequential,
            verbose=True
        )

        # Test execution
        # output = self.execute_crew()
        # self.assertCrewCompletedSuccessfully(output)
        # self.assertCrewOutputMatches(output, "article")
```

**Key Methods:**
- `add_test_agent()`: Add agent to test crew
- `add_test_task()`: Add task to test workflow
- `create_test_crew()`: Create crew with agents and tasks
- `execute_crew()`: Execute crew workflow
- `assertCrewCompletedSuccessfully()`: Verify successful execution
- `assertCrewOutputMatches()`: Check output content
- `measure_crew_performance()`: Get performance metrics

### 3. Specialized Assertions

Domain-specific assertions for AI agent testing.

```python
from crewai.testing.assertions import (
    assert_agent_response_contains,
    assert_agent_response_quality,
    assert_crew_completed_successfully,
    assert_crew_output_matches,
    assert_output_format,
    assert_no_hallucination,
)

# Usage examples
assert_agent_response_contains(output, "expected content", case_sensitive=False)
assert_agent_response_quality(output, task, min_score=8.0)
assert_output_format(output, "json")  # or "markdown", "yaml", etc.
assert_crew_output_matches(crew_output, r"pattern.*regex", regex=True)
```

### 4. Mock Utilities

Mock agents and tools for isolated testing.

```python
from crewai.testing import MockAgent, MockTool

# Create mock agent with predefined responses
mock_agent = MockAgent(
    role="Test Agent",
    responses=["Response 1", "Response 2", "Response 3"]
)

# Create mock tool
mock_tool = MockTool(
    name="search_tool",
    description="Mock search functionality",
    return_value="Mock search results"
)

# Test tool usage
result = mock_tool._run("query")
assert mock_tool.was_called()
assert mock_tool.call_count() == 1
```

### 5. Test Runner

Discover and execute CrewAI tests with detailed reporting.

```python
from crewai.testing import TestRunner

# Create test runner
runner = TestRunner(verbosity=2)

# Discover tests
suite = runner.discover_crewai_tests(test_dir="tests")

# Run tests
result = runner.run_tests(suite)

# Print results
runner.print_results(result)

# Generate HTML report
runner.generate_report(result, "test_report.html")
```

## CLI Commands

### crewai test-framework

Run the CrewAI testing framework for agent and crew tests.

```bash
crewai test-framework [OPTIONS]
```

**Options:**
- `-d, --test-dir TEXT`: Directory containing test files (default: "tests")
- `-p, --pattern TEXT`: Pattern for test file names (default: "test_*.py")
- `-v, --verbosity INTEGER`: Output verbosity level 0-2 (default: 2)
- `--report`: Generate HTML test report
- `--report-file TEXT`: HTML report file path (default: "crewai_test_report.html")

**Examples:**

```bash
# Run all tests with default settings
crewai test-framework

# Run tests in specific directory
crewai test-framework -d integration_tests

# Run with custom pattern and generate report
crewai test-framework -p "*_test.py" --report

# Quiet mode with custom report file
crewai test-framework -v 0 --report --report-file results.html
```

## Testing Patterns

### 1. Agent Behavior Testing

Test individual agent capabilities and responses:

```python
class TestAnalystAgent(AgentTestCase):
    def test_data_analysis_capability(self):
        task = self.create_test_task(
            description="Analyze sales data for Q4 trends",
            expected_output="Sales analysis with trend insights"
        )

        # Mock execution result
        mock_analysis = """
        Q4 Sales Analysis:
        - 15% increase in revenue compared to Q3
        - Mobile sales grew 25% year-over-year
        - Top performing regions: West Coast, Northeast
        """

        self.assertAgentResponseContains(mock_analysis, "15% increase")
        self.assertAgentResponseContains(mock_analysis, "Mobile sales")

    def test_response_format(self):
        formatting_task = self.create_test_task(
            description="Generate JSON report of key metrics",
            expected_output="Valid JSON with metrics data"
        )

        mock_json = '{"revenue": 1500000, "growth": 0.15, "regions": ["west", "northeast"]}'
        self.assertOutputFormat(mock_json, "json")
```

### 2. Crew Collaboration Testing

Test multi-agent workflows and collaboration:

```python
class TestMarketingCrew(CrewTestCase):
    def test_campaign_creation_workflow(self):
        # Set up marketing team
        strategist = self.add_test_agent(
            role="Marketing Strategist",
            goal="Develop marketing strategies"
        )

        copywriter = self.add_test_agent(
            role="Copywriter",
            goal="Create compelling marketing copy"
        )

        # Define workflow tasks
        strategy_task = self.add_test_task(
            description="Create marketing strategy for new product",
            expected_output="Comprehensive marketing strategy",
            agent=strategist
        )

        copy_task = self.add_test_task(
            description="Write marketing copy based on strategy",
            expected_output="Engaging marketing materials",
            agent=copywriter
        )

        # Create and test crew
        crew = self.create_test_crew(
            tasks=[strategy_task, copy_task],
            process=Process.sequential
        )

        # Mock execution and validation
        # output = self.execute_crew()
        # self.assertCrewCompletedSuccessfully(output)
```

### 3. Quality Assurance Testing

Validate output quality and format:

```python
class TestContentQuality(AgentTestCase):
    def test_content_meets_standards(self):
        content_task = self.create_test_task(
            description="Write blog post about sustainable technology",
            expected_output="SEO-optimized blog post with engaging content"
        )

        mock_blog_post = """
        # Sustainable Technology: Shaping Our Future

        Sustainable technology represents the intersection of innovation...
        [Content continues with proper structure, keywords, etc.]
        """

        # Quality checks
        self.assertOutputFormat(mock_blog_post, "markdown")
        self.assertAgentResponseContains(mock_blog_post, "sustainable")
        # self.assertAgentResponseQuality(mock_blog_post, content_task, min_score=8.5)
```

### 4. Error Handling and Edge Cases

Test system behavior under failure conditions:

```python
class TestErrorHandling(CrewTestCase):
    def test_crew_handles_task_failure(self):
        # Create scenario with potential failure
        risky_task = self.add_test_task(
            description="Process malformed data",
            expected_output="Processed results or error handling"
        )

        error_crew = self.create_test_crew(tasks=[risky_task])

        # Test error handling
        # This would test actual error scenarios
        pass

    def test_agent_graceful_degradation(self):
        # Test agent behavior when tools are unavailable
        pass
```

## Best Practices

### 1. Test Organization

Organize tests by functionality and scope:

```
tests/
├── agents/
│   ├── test_research_agent.py
│   ├── test_writing_agent.py
│   └── test_analysis_agent.py
├── crews/
│   ├── test_content_crew.py
│   ├── test_analysis_crew.py
│   └── test_support_crew.py
├── integration/
│   ├── test_end_to_end.py
│   └── test_performance.py
└── utils/
    └── test_helpers.py
```

### 2. Test Data Management

Use consistent test data and scenarios:

```python
# test_data.py
SAMPLE_RESEARCH_TOPICS = [
    "artificial intelligence trends",
    "renewable energy adoption",
    "remote work productivity"
]

EXPECTED_OUTPUTS = {
    "research": "Comprehensive analysis with sources",
    "summary": "Concise summary of key points",
    "report": "Formatted report with recommendations"
}

# Use in tests
class TestResearcher(AgentTestCase):
    def test_multiple_topics(self):
        for topic in SAMPLE_RESEARCH_TOPICS:
            with self.subTest(topic=topic):
                task = self.create_test_task(
                    description=f"Research {topic}",
                    expected_output=EXPECTED_OUTPUTS["research"]
                )
                # Test logic here
```

### 3. Mock Strategy

Use mocks strategically for isolation and reliability:

```python
from crewai.testing import MockAgent, MockTool, patch_agent_llm

class TestWithMocks(AgentTestCase):
    def test_agent_with_mock_tools(self):
        # Create mock tools
        mock_search = MockTool(
            name="search",
            return_value="Mock search results"
        )

        # Create agent with mock tools
        agent = self.create_test_agent(
            role="Researcher",
            tools=[mock_search]
        )

        # Test with predictable tool behavior
        # task execution and verification
```

### 4. Performance Testing

Include performance benchmarks:

```python
import time
from crewai.testing import CrewTestCase

class TestPerformance(CrewTestCase):
    def test_crew_execution_time(self):
        # Set up performance test crew
        crew = self.create_test_crew()

        # Measure execution time
        start_time = time.time()
        # output = self.execute_crew()
        end_time = time.time()

        execution_time = end_time - start_time
        self.assertLess(execution_time, 30.0, "Crew execution took too long")

        # Verify performance metrics
        # metrics = self.measure_crew_performance(output)
        # self.assertGreater(metrics['collaboration_score'], 0.8)
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: CrewAI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest

    - name: Run CrewAI Tests
      run: |
        crewai test-framework --report --report-file test_results.html

    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: test_results.html
```

### Integration Testing

```python
# tests/integration/test_production_scenarios.py
from crewai.testing import CrewTestCase

class TestProductionScenarios(CrewTestCase):
    """Integration tests for production-like scenarios."""

    def test_customer_support_workflow(self):
        """Test complete customer support resolution workflow."""
        # Set up realistic customer support crew
        ticket_analyzer = self.add_test_agent(
            role="Support Ticket Analyzer",
            goal="Categorize and prioritize support tickets"
        )

        solution_specialist = self.add_test_agent(
            role="Solution Specialist",
            goal="Provide technical solutions and guidance"
        )

        # Test with real-world scenarios
        urgent_ticket = self.add_test_task(
            description="Customer reports application crash during data export",
            expected_output="Prioritized ticket with initial solution recommendations"
        )

        # Execute and validate end-to-end workflow
        crew = self.create_test_crew(
            agents=[ticket_analyzer, solution_specialist],
            tasks=[urgent_ticket]
        )

        # Comprehensive validation
        # output = self.execute_crew()
        # self.assertCrewCompletedSuccessfully(output)
        # self.assertCrewOutputMatches(output, "solution")
        # self.assertCrewOutputMatches(output, "priority")
```

## Advanced Features

### Custom Evaluators

Extend the framework with custom evaluation logic:

```python
from crewai.experimental.evaluation.base_evaluator import BaseEvaluator, EvaluationScore

class CustomDomainEvaluator(BaseEvaluator):
    def evaluate(self, task_description: str, expected_output: str, actual_output: str) -> EvaluationScore:
        # Custom evaluation logic
        score = self._calculate_domain_specific_score(actual_output)
        feedback = self._generate_domain_feedback(actual_output)

        return EvaluationScore(
            score=score,
            feedback=feedback
        )

# Use in tests
class TestWithCustomEvaluator(AgentTestCase):
    def test_domain_specific_quality(self):
        evaluator = CustomDomainEvaluator()
        task = self.create_test_task("Domain-specific task")

        # Custom evaluation
        # score = evaluator.evaluate(task.description, task.expected_output, actual_output)
        # self.assertGreater(score.score, 7.0)
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ImportError: No module named 'crewai.testing'
   ```
   Solution: Ensure you're using the latest CrewAI version with testing framework support.

2. **Test Discovery Issues**
   ```
   No CrewAI tests found
   ```
   Solution:
   - Verify test files start with `test_`
   - Check test classes inherit from `AgentTestCase` or `CrewTestCase`
   - Ensure test methods start with `test_`

3. **Mock Setup Problems**
   ```
   Mock agents not behaving as expected
   ```
   Solution:
   - Verify mock responses are properly configured
   - Check agent execution is using mocked components
   - Review mock tool setup and return values

### Debug Mode

Run tests with maximum verbosity for debugging:

```bash
crewai test-framework -v 2 --test-dir tests/debug
```

Enable detailed logging in test code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

class DebugTest(AgentTestCase):
    def test_with_debug(self):
        # Add debug logging
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting test execution")

        # Test logic with debug output
```

## Contributing

To contribute to the testing framework:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/testing-enhancement`
3. Add tests for new functionality
4. Ensure all tests pass: `crewai test-framework`
5. Submit pull request

## License

This testing framework is part of CrewAI and follows the same MIT license.