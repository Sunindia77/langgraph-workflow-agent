"""Unit tests for agents and tools."""
import asyncio
import pytest
import logging

from coordinator_agent import CoordinatorAgent
from researcher_agent import ResearcherAgent
from analyzer_agent import AnalyzerAgent
from state_schemas import WorkflowState, AgentConfig
from search_tools import SearchToolManager, WebSearchTool, DocumentSearchTool
from analysis_tools import AnalysisToolManager


class TestAgents:
    """Test suite for agents."""
    
    @pytest.mark.asyncio
    async def test_researcher_agent_execution(self):
        """Test researcher agent can execute."""
        researcher = ResearcherAgent()
        state = WorkflowState(query="test query")
        
        result = await researcher.execute(state)
        
        assert result.query == "test query"
        assert len(result.messages) > 0
        assert result.current_agent == "researcher"
        assert len(result.search_results) > 0
    
    @pytest.mark.asyncio
    async def test_analyzer_agent_execution(self):
        """Test analyzer agent can execute."""
        analyzer = AnalyzerAgent()
        state = WorkflowState(
            query="test query",
            search_results=[
                {"title": "Test", "snippet": "content", "url": "http://test.com"}
            ]
        )
        
        result = await analyzer.execute(state)
        
        assert result.query == "test query"
        assert result.current_agent == "analyzer"
        assert len(result.messages) > 0
    
    @pytest.mark.asyncio
    async def test_coordinator_agent_full_workflow(self):
        """Test coordinator orchestrates full workflow."""
        coordinator = CoordinatorAgent()
        state = WorkflowState(query="AI trends")
        
        result = await coordinator.execute(state)
        
        # Check all phases completed
        assert result.final_answer is not None
        assert len(result.messages) > 0
        assert len(result.search_results) > 0


class TestSearchTools:
    """Test suite for search tools."""
    
    @pytest.mark.asyncio
    async def test_web_search_tool(self):
        """Test web search tool."""
        tool = WebSearchTool()
        results = await tool.search("test query", max_results=5)
        
        assert len(results) <= 5
        assert all("title" in r for r in results)
        assert all("url" in r for r in results)
    
    @pytest.mark.asyncio
    async def test_document_search_tool(self):
        """Test document search tool."""
        docs = {
            "doc1": "AI is transforming industries",
            "doc2": "Machine learning algorithms are powerful"
        }
        tool = DocumentSearchTool(docs)
        
        results = await tool.search("AI", max_results=10)
        
        assert len(results) > 0
        assert results[0]["doc_id"] == "doc1"
    
    @pytest.mark.asyncio
    async def test_search_manager_parallel_search(self):
        """Test search manager parallel search."""
        manager = SearchToolManager()
        manager.register_tool(WebSearchTool())
        manager.register_tool(DocumentSearchTool())
        
        results = await manager.parallel_search("test query")
        
        assert "web_search" in results or len(results) > 0


class TestAnalysisTools:
    """Test suite for analysis tools."""
    
    @pytest.mark.asyncio
    async def test_data_aggregator(self):
        """Test data aggregator tool."""
        manager = AnalysisToolManager()
        
        data = [
            {"source": "web", "value": 1},
            {"source": "web", "value": 2},
            {"source": "api", "value": 3}
        ]
        
        result = await manager.analyze("data_aggregator", data)
        
        assert result["total_items"] == 3
        assert len(result["summary"]["sources"]) > 0
    
    @pytest.mark.asyncio
    async def test_validator_tool(self):
        """Test validator tool."""
        manager = AnalysisToolManager()
        
        data = [
            {"field1": "value1", "field2": "value2"},
            {"field1": "value3", "field2": "value4"}
        ]
        
        result = await manager.analyze("validator", data)
        
        assert "status" in result
        assert "score" in result
    
    @pytest.mark.asyncio
    async def test_analysis_pipeline(self):
        """Test analysis pipeline."""
        manager = AnalysisToolManager()
        
        data = [
            {"value": 1, "category": "A"},
            {"value": 2, "category": "A"},
            {"value": 3, "category": "B"}
        ]
        
        result = await manager.pipeline(
            data,
            ["data_aggregator", "pattern_detector", "validator"]
        )
        
        assert len(result["steps"]) == 3
        assert "final_result" in result


class TestWorkflowState:
    """Test suite for workflow state."""
    
    def test_workflow_state_creation(self):
        """Test creating workflow state."""
        state = WorkflowState(query="test")
        
        assert state.query == "test"
        assert state.messages == []
        assert state.search_results == []
        assert state.tool_calls == []
    
    def test_workflow_state_validation(self):
        """Test state validation with Pydantic."""
        # Valid state
        state = WorkflowState(query="test")
        assert state.query == "test"
        
        # Pydantic will validate types


def test_agent_config():
    """Test agent configuration."""
    config = AgentConfig(
        name="test_agent",
        description="Test",
        tools=["tool1", "tool2"]
    )
    
    assert config.name == "test_agent"
    assert len(config.tools) == 2


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
