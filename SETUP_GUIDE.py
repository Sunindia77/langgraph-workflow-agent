"""
LangGraph Multi-Agent Workflow Agent
====================================

A production-ready agentic AI system featuring:
- Multi-agent orchestration (Researcher → Analyzer → Coordinator)
- Tool calling with search, retrieval, and analysis
- Retrieval-Augmented Generation (RAG) integration
- Robust error handling and state management
- Full async/await implementation

PROJECT STRUCTURE
=================

Core Files:
  - base_agent.py           Base class for all agents
  - coordinator_agent.py    Orchestrates multi-agent workflow
  - researcher_agent.py     Gathers information
  - analyzer_agent.py       Analyzes and synthesizes data

Tools:
  - search_tools.py         Web search, document search, API calls
  - retrieval_tools.py      Vector retrieval, RAG, hybrid search
  - analysis_tools.py       Data aggregation, synthesis, validation

State & Config:
  - state_schemas.py        Pydantic models for workflow state
  - env_config.py          Environment and configuration
  - logging_setup.py       Structured logging

Entry Points:
  - main_workflow.py       Main CLI interface
  - example_basic_workflow.py      Simple example
  - example_advanced_workflow.py   Multi-query example

Tests:
  - test_agents.py         Comprehensive test suite

INSTALLATION
============

1. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements_langgraph.txt

3. Create .env file:
   cp .env.example .env
   # Edit .env with your API keys

QUICK START
===========

1. Basic Usage (Command Line):
   python main_workflow.py "What are the latest AI trends?"

2. Interactive Mode:
   python main_workflow.py
   # Then enter queries interactively

3. Run Basic Example:
   python example_basic_workflow.py

4. Run Advanced Example:
   python example_advanced_workflow.py

5. Run Tests:
   pytest test_agents.py -v

ARCHITECTURE
============

Workflow Phases:

1. RESEARCH Phase
   - Query enters Researcher Agent
   - Web search, document search, API queries
   - Results aggregated and stored in state

2. ANALYSIS Phase
   - Results passed to Analyzer Agent
   - Retrieval-augmented generation
   - Pattern detection, data validation
   - Analysis pipeline executed

3. SYNTHESIS Phase
   - Coordinator synthesizes all results
   - Generates final answer
   - Returns comprehensive response

4. COMPLETE
   - Workflow finished
   - State contains all intermediate results

USAGE EXAMPLES
==============

Command Line:
  python main_workflow.py "Explain machine learning"

Python Code:
  import asyncio
  from coordinator_agent import CoordinatorAgent
  from state_schemas import WorkflowState
  
  async def main():
      coordinator = CoordinatorAgent()
      state = WorkflowState(query="Your query here")
      result = await coordinator.execute(state)
      print(result.final_answer)
  
  asyncio.run(main())

Custom Agent:
  from base_agent import BaseAgent
  from state_schemas import AgentConfig, WorkflowState
  
  class CustomAgent(BaseAgent):
      async def execute(self, state: WorkflowState) -> WorkflowState:
          # Your logic here
          return state
      
      async def call_tool(self, tool_name: str, **kwargs):
          # Tool implementation
          return result

Add Custom Tool:
  from search_tools import SearchTool, SearchToolManager
  
  class MySearchTool(SearchTool):
      def __init__(self):
          super().__init__("my_tool", "Description")
      
      async def search(self, query: str, **kwargs):
          # Implementation
          return results
  
  manager = SearchToolManager()
  manager.register_tool(MySearchTool())
  results = await manager.search("my_tool", "query")

CONFIGURATION
=============

Environment Variables (.env):

LLM_PROVIDER:     Which LLM to use (openai, anthropic)
OPENAI_API_KEY:   Your OpenAI API key
ANTHROPIC_API_KEY: Your Anthropic API key
LLM_MODEL:        Model to use (gpt-4, claude-3, etc)
VECTOR_DB_TYPE:   Vector database (chroma, pinecone)
CHROMA_DB_PATH:   Path to Chroma database
AGENT_TIMEOUT:    Timeout in seconds for agent execution
MAX_RETRIES:      Maximum retry attempts
LOG_LEVEL:        Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE:         Path to log file

WORKFLOW STATE
==============

The WorkflowState object tracks:
  - query: Original user query
  - messages: All messages in conversation
  - tool_calls: Record of all tool executions
  - search_results: Results from search phase
  - analysis_results: Results from analysis phase
  - retrieval_context: Retrieved documents for RAG
  - final_answer: Synthesized final response
  - metadata: Custom metadata
  - current_agent: Currently executing agent

ADVANCED FEATURES
=================

Parallel Search:
  results = await manager.parallel_search(
      "query",
      tool_names=["web_search", "document_search"]
  )

Analysis Pipeline:
  result = await manager.pipeline(
      data,
      ["data_aggregator", "synthesis", "validator"]
  )

RAG Context:
  context = await rag_context.get_context(
      query="Your query",
      top_k=10,
      use_cache=True
  )

Hybrid Retrieval:
  hybrid = HybridRetriever()
  hybrid.add_retriever(retriever1, weight=0.6)
  hybrid.add_retriever(retriever2, weight=0.4)
  results = await hybrid.retrieve(query)

TESTING
=======

Run all tests:
  pytest test_agents.py -v

Run specific test class:
  pytest test_agents.py::TestAgents -v

Run with coverage:
  pytest test_agents.py --cov

PERFORMANCE TIPS
================

1. Use caching for repeated queries
2. Run parallel searches with parallel_search()
3. Configure appropriate timeouts
4. Use analysis pipelines instead of individual calls
5. Monitor log files for bottlenecks
6. Consider vector DB persistence

TROUBLESHOOTING
===============

No results found:
  - Check search tools are registered
  - Verify query is specific enough
  - Check network connectivity

Analysis fails:
  - Verify search results exist
  - Check data validation rules
  - Review error logs

Slow execution:
  - Increase timeout values
  - Use parallel search
  - Check network latency

EXTENDING THE SYSTEM
====================

Create Custom Agent:
  1. Inherit from BaseAgent
  2. Implement execute() and call_tool()
  3. Use provided tools or create new ones
  4. Register with coordinator

Create Custom Tool:
  1. Choose tool category (SearchTool, RetrieverTool, AnalysisTool)
  2. Implement abstract methods
  3. Register with appropriate manager
  4. Use in agents

Create Tool Manager:
  1. Create manager class
  2. Register tools
  3. Implement execute/pipeline methods
  4. Use in agents

CONTRIBUTING
============

To contribute:
1. Follow existing code style
2. Add type hints
3. Write tests for new features
4. Update documentation
5. Use async/await patterns

LICENSE
=======

MIT

SUPPORT
=======

For issues:
1. Check logs first
2. Review error messages
3. Check this documentation
4. Create GitHub issue

For questions:
1. Review examples
2. Check architecture documentation
3. Look at test cases
"""

if __name__ == "__main__":
    print(__doc__)
