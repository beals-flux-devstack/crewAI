"""
Example test file demonstrating agent behavior testing with CrewAI Testing Framework.

This file shows how to test individual agents using the AgentTestCase base class
and various assertion methods.
"""

from crewai import Agent, Task
from crewai.testing import AgentTestCase


class TestResearchAgent(AgentTestCase):
    """Test cases for a research agent."""

    def setUp(self) -> None:
        """Set up test environment with a research agent."""
        super().setUp()

        # Create a test agent
        self.create_test_agent(
            role="Senior Research Analyst",
            goal="Conduct thorough research and provide accurate insights",
            backstory="You are an experienced research analyst with expertise in gathering and analyzing information from various sources.",
        )

    def test_agent_provides_research_insights(self) -> None:
        """Test that research agent provides meaningful insights."""
        # Create a test task
        task = self.create_test_task(
            description="Research the latest trends in artificial intelligence",
            expected_output="A comprehensive analysis of current AI trends with key insights and supporting evidence",
        )

        # Execute the task (in a real implementation)
        # For now, this is a conceptual example
        # output = self.execute_agent_task(task)

        # Mock output for demonstration
        mock_output = "AI trends in 2024 include: 1) Multimodal AI systems, 2) AI governance frameworks, 3) Edge AI deployment..."

        # Test assertions
        self.assertAgentResponseContains(mock_output, "AI trends")
        self.assertAgentResponseContains(mock_output, "2024", case_sensitive=True)

        # Test output format
        self.assertOutputFormat(mock_output, "text")

    def test_agent_handles_complex_queries(self) -> None:
        """Test agent's ability to handle complex research queries."""
        complex_task = self.create_test_task(
            description="Analyze the impact of quantum computing on cybersecurity, including potential risks and mitigation strategies",
            expected_output="Detailed analysis covering quantum computing's impact on encryption, potential security vulnerabilities, and recommended defensive strategies",
        )

        # Mock complex response
        mock_response = """
        Quantum computing presents both opportunities and challenges for cybersecurity:

        Impact on Encryption:
        - Current RSA encryption vulnerable to quantum attacks via Shor's algorithm
        - Timeline: 10-15 years for cryptographically relevant quantum computers

        Risks:
        1. Cryptographic obsolescence
        2. Data harvesting for future decryption
        3. Infrastructure vulnerabilities

        Mitigation Strategies:
        1. Post-quantum cryptography implementation
        2. Hybrid security models
        3. Quantum key distribution
        """

        # Verify comprehensive coverage
        self.assertAgentResponseContains(mock_response, "encryption")
        self.assertAgentResponseContains(mock_response, "risks")
        self.assertAgentResponseContains(mock_response, "mitigation")

        # Verify structured output
        self.assertTrue("1." in mock_response and "2." in mock_response)

    def test_agent_response_quality(self) -> None:
        """Test the quality of agent responses."""
        quality_task = self.create_test_task(
            description="Provide recommendations for implementing AI ethics in organizations",
            expected_output="Practical, actionable recommendations for establishing AI ethics frameworks in corporate environments",
        )

        mock_high_quality_response = """
        Implementing AI Ethics in Organizations: A Practical Framework

        1. Governance Structure
        - Establish AI Ethics Committee with diverse expertise
        - Define clear roles and responsibilities
        - Create escalation procedures for ethical concerns

        2. Policy Development
        - Draft comprehensive AI ethics policy
        - Address bias, transparency, and accountability
        - Include regular review and update mechanisms

        3. Implementation Strategy
        - Conduct ethics training for development teams
        - Implement bias testing protocols
        - Establish continuous monitoring systems

        4. Stakeholder Engagement
        - Regular consultation with affected communities
        - Transparent communication about AI systems
        - Feedback mechanisms for continuous improvement

        These recommendations provide a structured approach to embedding ethical considerations throughout the AI development lifecycle.
        """

        # Test response quality (this would use actual evaluators in practice)
        # self.assertAgentResponseQuality(mock_high_quality_response, quality_task, min_score=8.0)

    def test_agent_tool_usage(self) -> None:
        """Test that agent uses tools appropriately."""
        # This would test tool usage in practice
        # For now, it's a conceptual demonstration
        research_task = self.create_test_task(
            description="Search for recent publications on machine learning",
            expected_output="List of recent ML publications with summaries",
        )

        # In a real test, this would verify the agent called search tools
        # self.assertAgentUsedTool("search_tool")
        pass


class TestWritingAgent(AgentTestCase):
    """Test cases for a writing agent."""

    def setUp(self) -> None:
        """Set up test environment with a writing agent."""
        super().setUp()

        self.create_test_agent(
            role="Technical Writer",
            goal="Create clear, comprehensive, and engaging technical documentation",
            backstory="You are a skilled technical writer with expertise in making complex topics accessible to various audiences.",
        )

    def test_markdown_output_format(self) -> None:
        """Test that writing agent produces valid Markdown."""
        writing_task = self.create_test_task(
            description="Write a technical guide for setting up a development environment",
            expected_output="A well-structured Markdown guide with headers, code blocks, and clear instructions",
        )

        mock_markdown_output = """
# Development Environment Setup Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed
- Git configured
- Text editor or IDE

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/example/project.git
cd project
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Verification

Run the following command to verify your setup:

```bash
python -m project --version
```

## Troubleshooting

- **Issue**: Import errors
- **Solution**: Ensure virtual environment is activated

## Next Steps

Once setup is complete, refer to the [Usage Guide](usage.md) for detailed instructions.
        """

        # Test Markdown format
        self.assertOutputFormat(mock_markdown_output, "markdown")

        # Test content quality
        self.assertAgentResponseContains(mock_markdown_output, "Prerequisites")
        self.assertAgentResponseContains(mock_markdown_output, "Installation Steps")
        self.assertAgentResponseContains(mock_markdown_output, "```bash")  # Code blocks

    def test_content_structure(self) -> None:
        """Test that written content has proper structure."""
        structure_task = self.create_test_task(
            description="Create a project README file",
            expected_output="Complete README with project description, installation instructions, usage examples, and contribution guidelines",
        )

        mock_readme = """
# Project Name

Brief description of the project and its purpose.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

Step-by-step installation instructions.

## Usage

Basic usage examples and API documentation.

## Contributing

Guidelines for contributing to the project.

## License

MIT License information.
        """

        # Test structural elements
        required_sections = ["Features", "Installation", "Usage", "Contributing", "License"]
        for section in required_sections:
            self.assertAgentResponseContains(mock_readme, section)


if __name__ == "__main__":
    import unittest
    unittest.main()