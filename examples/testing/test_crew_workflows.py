"""
Example test file demonstrating crew workflow testing with CrewAI Testing Framework.

This file shows how to test crew collaboration, task sequences, and
end-to-end workflows using the CrewTestCase base class.
"""

from crewai import Process
from crewai.testing import CrewTestCase


class TestContentCreationCrew(CrewTestCase):
    """Test cases for a content creation crew workflow."""

    def setUp(self) -> None:
        """Set up test environment with content creation crew."""
        super().setUp()

        # Create agents for content creation workflow
        self.researcher = self.add_test_agent(
            role="Content Researcher",
            goal="Gather accurate and relevant information for content creation",
            backstory="You are a meticulous researcher who ensures all content is well-researched and factually accurate.",
        )

        self.writer = self.add_test_agent(
            role="Content Writer",
            goal="Create engaging and well-structured content based on research",
            backstory="You are a skilled writer who transforms research into compelling, readable content.",
        )

        self.editor = self.add_test_agent(
            role="Content Editor",
            goal="Review and polish content for clarity, accuracy, and style",
            backstory="You are an experienced editor with an eye for detail and a commitment to quality.",
        )

    def test_sequential_content_workflow(self) -> None:
        """Test sequential content creation workflow."""
        # Define the content creation tasks
        research_task = self.add_test_task(
            description="Research the latest developments in renewable energy technology",
            expected_output="Comprehensive research summary with key findings, statistics, and recent developments",
            agent=self.researcher,
        )

        writing_task = self.add_test_task(
            description="Write a 1000-word article about renewable energy based on the research",
            expected_output="Well-structured article with introduction, main points, and conclusion",
            agent=self.writer,
        )

        editing_task = self.add_test_task(
            description="Edit and polish the article for publication",
            expected_output="Final polished article ready for publication with proper formatting and style",
            agent=self.editor,
        )

        # Create crew with sequential process
        crew = self.create_test_crew(
            agents=[self.researcher, self.writer, self.editor],
            tasks=[research_task, writing_task, editing_task],
            process=Process.sequential,
            verbose=True,
        )

        # Mock crew execution and output
        mock_crew_output_raw = """
        # Renewable Energy: The Future is Now

        ## Introduction

        Renewable energy technology has reached unprecedented levels of efficiency and affordability in 2024. Recent developments in solar, wind, and storage technologies are reshaping the global energy landscape.

        ## Key Developments

        ### Solar Technology Advances
        - Perovskite solar cells achieving 31% efficiency
        - Floating solar installations growing 22% annually
        - Agrivoltaics combining agriculture with solar generation

        ### Wind Energy Breakthroughs
        - Offshore wind turbines reaching 15MW capacity
        - Vertical axis turbines for urban applications
        - Advanced materials reducing maintenance costs

        ### Energy Storage Revolution
        - Lithium-iron-phosphate batteries cost reduction of 40%
        - Grid-scale storage deployments doubling yearly
        - Innovative technologies like gravity and compressed air storage

        ## Economic Impact

        The renewable energy sector now employs over 13 million people globally, with job growth outpacing traditional energy sectors by 300%. Investment in renewables reached $1.8 trillion in 2024, representing 70% of all energy investments.

        ## Challenges and Solutions

        While renewable energy shows tremendous promise, challenges remain:
        - Grid stability and intermittency issues
        - Raw material supply chain concerns
        - Policy and regulatory frameworks

        Innovative solutions are emerging, including smart grid technologies, diversified supply chains, and supportive government policies.

        ## Conclusion

        The renewable energy revolution is accelerating, driven by technological innovation, economic viability, and environmental necessity. The next decade will likely see renewables become the dominant global energy source.
        """

        # Simulate crew execution (in practice, this would be actual execution)
        # crew_output = self.execute_crew(inputs={"topic": "renewable energy"})

        # Mock crew output object for testing
        class MockCrewOutput:
            def __init__(self, raw_content):
                self.raw = raw_content
                self.tasks_output = []

        mock_output = MockCrewOutput(mock_crew_output_raw)

        # Test crew completion
        self.assertCrewCompletedSuccessfully(mock_output)

        # Test output content
        self.assertCrewOutputMatches(mock_output, "Renewable Energy")
        self.assertCrewOutputMatches(mock_output, "solar")
        self.assertCrewOutputMatches(mock_output, "wind")

        # Test output format (Markdown)
        self.assertCrewOutputFormat(mock_output, "markdown")

        # Test comprehensive content
        required_sections = ["Introduction", "Key Developments", "Economic Impact", "Conclusion"]
        for section in required_sections:
            self.assertCrewOutputMatches(mock_output, section)

    def test_collaborative_research_crew(self) -> None:
        """Test collaborative research workflow."""
        # Create a collaborative scenario
        agent_configs = [
            {
                "role": "Primary Researcher",
                "goal": "Lead research efforts and coordinate with team",
                "backstory": "Senior researcher with project management experience",
            },
            {
                "role": "Data Analyst",
                "goal": "Analyze data and provide statistical insights",
                "backstory": "Expert in data analysis and statistical modeling",
            },
            {
                "role": "Subject Matter Expert",
                "goal": "Provide domain expertise and validate findings",
                "backstory": "Industry expert with deep knowledge of the research domain",
            },
        ]

        task_configs = [
            {
                "description": "Define research methodology and coordinate team efforts",
                "expected_output": "Research plan with clear methodology and team coordination strategy",
            },
            {
                "description": "Analyze collected data and generate statistical insights",
                "expected_output": "Statistical analysis report with key findings and visualizations",
            },
            {
                "description": "Review findings and provide expert validation",
                "expected_output": "Expert review with validation of findings and recommendations",
            },
        ]

        # Create collaborative scenario
        agents, tasks = self.create_collaborative_scenario(
            scenario_name="collaborative_research",
            agent_configs=agent_configs,
            task_configs=task_configs,
        )

        # Create crew
        collab_crew = self.create_test_crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
        )

        # Mock execution results
        mock_collab_output = """
        ## Research Methodology and Coordination Plan

        ### Methodology
        - Mixed-methods approach combining quantitative and qualitative analysis
        - Data collection through surveys, interviews, and secondary sources
        - Three-phase execution with regular team checkpoints

        ### Team Coordination
        - Weekly progress meetings
        - Shared data repository and documentation
        - Clear role definitions and deliverable timelines

        ## Statistical Analysis Report

        ### Key Findings
        - 78% increase in efficiency metrics
        - Statistically significant correlation (p<0.05) between variables A and B
        - Identified three primary trend patterns in the dataset

        ### Data Visualizations
        - Trend analysis charts showing temporal patterns
        - Correlation matrices highlighting variable relationships
        - Distribution plots revealing data characteristics

        ## Expert Validation and Recommendations

        ### Validation Results
        - Research methodology aligns with industry best practices
        - Statistical analysis methodology is sound and appropriate
        - Findings are consistent with domain expertise

        ### Recommendations
        1. Implement findings in pilot program
        2. Monitor key performance indicators
        3. Scale successful interventions organization-wide
        """

        class MockCollabOutput:
            def __init__(self, raw_content):
                self.raw = raw_content
                self.tasks_output = [
                    type('TaskOutput', (), {'error': None})(),
                    type('TaskOutput', (), {'error': None})(),
                    type('TaskOutput', (), {'error': None})(),
                ]

        mock_output = MockCollabOutput(mock_collab_output)

        # Test collaboration success
        self.assertCrewCompletedSuccessfully(mock_output)

        # Test that all team contributions are present
        team_contributions = ["Methodology", "Statistical Analysis", "Expert Validation"]
        for contribution in team_contributions:
            self.assertCrewOutputMatches(mock_output, contribution)

        # Test collaborative elements
        self.assertCrewOutputMatches(mock_output, "team")
        self.assertCrewOutputMatches(mock_output, "coordination")

    def test_error_handling_in_crew(self) -> None:
        """Test crew behavior when tasks fail."""
        # Create a scenario with potential failures
        error_prone_task = self.add_test_task(
            description="Process invalid data format",
            expected_output="Processed results",
            agent=self.researcher,
        )

        error_crew = self.create_test_crew(
            tasks=[error_prone_task],
        )

        # Mock failed output
        class MockFailedOutput:
            def __init__(self):
                self.raw = "Partial results before failure"
                self.tasks_output = [
                    type('TaskOutput', (), {'error': 'Invalid data format'})(),
                ]

        # This would test error handling
        # failed_output = MockFailedOutput()
        # with self.assertRaises(AssertionError):
        #     self.assertCrewCompletedSuccessfully(failed_output)

    def test_crew_performance_metrics(self) -> None:
        """Test crew performance measurement."""
        # Create a performance test scenario
        perf_crew = self.create_test_crew()

        # Mock successful execution
        class MockPerfOutput:
            def __init__(self):
                self.raw = "Performance test results"
                self.tasks_output = [
                    type('TaskOutput', (), {'error': None})() for _ in range(3)
                ]

        mock_output = MockPerfOutput()

        # Measure performance
        metrics = self.measure_crew_performance(mock_output)

        # Verify performance structure
        expected_metrics = ['execution_time', 'total_tasks', 'successful_tasks', 'agent_utilization', 'collaboration_score']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)

        # Test specific values
        self.assertEqual(metrics['total_tasks'], len(self.test_tasks))
        self.assertEqual(metrics['successful_tasks'], 3)


class TestAnalyticsCrew(CrewTestCase):
    """Test cases for analytics and reporting crew."""

    def test_data_analysis_pipeline(self) -> None:
        """Test end-to-end data analysis pipeline."""
        # Create analytics team
        data_collector = self.add_test_agent(
            role="Data Collection Specialist",
            goal="Gather and validate data from multiple sources",
            backstory="Expert in data collection with attention to data quality and integrity",
        )

        analyst = self.add_test_agent(
            role="Senior Data Analyst",
            goal="Perform comprehensive data analysis and generate insights",
            backstory="Experienced analyst skilled in statistical methods and data interpretation",
        )

        reporter = self.add_test_agent(
            role="Report Generator",
            goal="Create clear, actionable reports from analysis results",
            backstory="Specialist in transforming complex analysis into understandable business insights",
        )

        # Define analytics pipeline tasks
        collection_task = self.add_test_task(
            description="Collect customer satisfaction data from surveys, reviews, and support tickets",
            expected_output="Clean dataset with validated customer satisfaction metrics",
            agent=data_collector,
        )

        analysis_task = self.add_test_task(
            description="Analyze customer satisfaction trends and identify key drivers",
            expected_output="Statistical analysis with trend identification and correlation analysis",
            agent=analyst,
        )

        reporting_task = self.add_test_task(
            description="Generate executive report with findings and recommendations",
            expected_output="Executive summary with key insights, trends, and actionable recommendations",
            agent=reporter,
        )

        # Create analytics crew
        analytics_crew = self.create_test_crew(
            agents=[data_collector, analyst, reporter],
            tasks=[collection_task, analysis_task, reporting_task],
            process=Process.sequential,
        )

        # Mock analytics output in JSON format
        mock_analytics_json = '''
        {
            "executive_summary": {
                "overall_satisfaction": 4.2,
                "trend": "improving",
                "key_insight": "Product quality is the primary driver of satisfaction"
            },
            "detailed_analysis": {
                "satisfaction_by_segment": {
                    "enterprise": 4.5,
                    "sme": 4.1,
                    "individual": 3.9
                },
                "correlation_analysis": {
                    "product_quality": 0.78,
                    "customer_support": 0.65,
                    "pricing": 0.43
                }
            },
            "recommendations": [
                "Focus quality improvements on individual customer segment",
                "Enhance customer support training",
                "Review pricing strategy for competitive positioning"
            ]
        }
        '''

        class MockAnalyticsOutput:
            def __init__(self, json_content):
                self.raw = json_content
                self.tasks_output = []

        mock_output = MockAnalyticsOutput(mock_analytics_json)

        # Test JSON format
        self.assertOutputFormat(mock_output, "json")

        # Test analytics content
        self.assertCrewOutputMatches(mock_output, "satisfaction")
        self.assertCrewOutputMatches(mock_output, "recommendations")
        self.assertCrewOutputMatches(mock_output, "correlation_analysis")


if __name__ == "__main__":
    import unittest
    unittest.main()