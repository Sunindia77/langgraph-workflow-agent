# LangGraph Multi-Agent Workflow - Quick Reference

## 🚀 Quick Start (5 minutes)

```bash
# 1. Navigate to project
cd c:\Users\HP\OneDrive\Documents\python

# 2. Install dependencies
pip install -r requirements_langgraph.txt

# 3. Configure environment
copy .env.example .env
# Edit .env with your API keys

# 4. Run a query
python main_workflow.py "What is AI?"

# 5. Or run interactively
python main_workflow.py
```

## 📚 What You Have

### Agents (3 types)
| Agent | Purpose | Tools Used |
|-------|---------|-----------|
| **Researcher** | Gather information | Web search, document search, APIs |
| **Analyzer** | Process & analyze data | Vector retrieval, pattern detection, validation |
| **Coordinator** | Orchestrate workflow | Delegates to Researcher & Analyzer |

### Tools (3 categories)
| Category | Tools | Purpose |
|----------|-------|---------|
| **Search** | WebSearchTool, DocumentSearchTool, APISearchTool | Find information |
| **Retrieval** | VectorStoreRetriever, HybridRetriever, RAGContext | Retrieve relevant documents |
| **Analysis** | DataAggregator, SynthesisTool, PatternDetector, Validator | Process & validate data |

## 🎯 Common Tasks

### Run Basic Workflow
```python
import asyncio
from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

async def main():
    coordinator = CoordinatorAgent()
    state = WorkflowState(query="Tell me about AI")
    result = await coordinator.execute(state)
    print(result.final_answer)

asyncio.run(main())
```

### Create Custom Agent
```python
from base_agent import BaseAgent
from state_schemas import AgentConfig, WorkflowState

class MyAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="my_agent",
            description="Does something custom",
            tools=["my_tool"]
        )
        super().__init__(config)
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        # Your logic here
        state = self.add_message(state, "assistant", "Result")
        return state
    
    async def call_tool(self, tool_name: str, **kwargs):
        # Tool implementation
        return result
```

### Add Custom Tool
```python
from search_tools import SearchTool, SearchToolManager

class MyTool(SearchTool):
    def __init__(self):
        super().__init__("my_tool", "My tool description")
    
    async def search(self, query: str, **kwargs):
        # Implementation
        results = [{"title": "Result", "content": "..."}]
        return results

# Register and use
manager = SearchToolManager()
manager.register_tool(MyTool())
results = await manager.search("my_tool", "query")
```

### Process Multiple Queries in Parallel
```python
import asyncio
from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

async def main():
    coordinator = CoordinatorAgent()
    queries = ["Query 1", "Query 2", "Query 3"]
    
    tasks = [
        coordinator.execute(WorkflowState(query=q))
        for q in queries
    ]
    
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result.final_answer)

asyncio.run(main())
```

## 📋 File Reference

| File | Purpose | Key Class |
|------|---------|-----------|
| `base_agent.py` | Agent foundation | `BaseAgent` |
| `coordinator_agent.py` | Workflow orchestration | `CoordinatorAgent` |
| `researcher_agent.py` | Information gathering | `ResearcherAgent` |
| `analyzer_agent.py` | Data analysis | `AnalyzerAgent` |
| `search_tools.py` | Search functionality | `SearchToolManager` |
| `retrieval_tools.py` | Document retrieval | `VectorStoreRetriever` |
| `analysis_tools.py` | Data processing | `AnalysisToolManager` |
| `state_schemas.py` | Data models | `WorkflowState` |
| `main_workflow.py` | CLI entry point | `run_workflow()` |

## 🔧 Configuration

**Environment Variables (.env):**
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4
AGENT_TIMEOUT=30
LOG_LEVEL=INFO
```

## 📊 Workflow Phases

```
1. RESEARCH
   └─ Gather info from sources

2. ANALYSIS  
   └─ Process & analyze data

3. SYNTHESIS
   └─ Create final answer

4. COMPLETE
   └─ Return results
```

## 🧪 Testing

```bash
# Run all tests
pytest test_agents.py -v

# Run specific test class
pytest test_agents.py::TestAgents -v

# Run with coverage
pytest test_agents.py --cov
```

## 📦 State Object

The `WorkflowState` tracks everything:

```python
state = WorkflowState(query="Your query")

# After execution:
state.messages          # Conversation history
state.search_results    # Found sources
state.analysis_results  # Analysis output
state.retrieval_context # Retrieved documents
state.tool_calls        # Tool execution records
state.final_answer      # Final synthesized answer
state.metadata          # Custom metadata
```

## 🔄 Agent Lifecycle

```
Create Agent
    ↓
Initialize with Config
    ↓
Execute (process state)
    ├─ Add message
    ├─ Call tools
    ├─ Process results
    └─ Update state
    ↓
Return updated state
```

## ⚙️ Tool Lifecycle

```
Register Tool with Manager
    ↓
Manager stores tool
    ↓
Call tool via manager
    ├─ Execute tool logic
    ├─ Handle errors
    └─ Return results
    ↓
Results added to state
```

## 🎓 Best Practices

1. **Use type hints** - All functions should have type annotations
2. **Add docstrings** - Explain what functions do
3. **Error handling** - Always wrap async calls in try/except
4. **Logging** - Use self.logger for debugging
5. **State tracking** - Update state for all operations
6. **Async patterns** - Use async/await consistently
7. **Testing** - Write tests for new features
8. **Configuration** - Use .env for secrets

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No results | Check query specificity, verify tools are registered |
| Slow execution | Use parallel search, check timeouts |
| Import errors | Verify all files in same directory, check imports |
| Missing dependencies | Run `pip install -r requirements_langgraph.txt` |
| API errors | Check .env file, verify API keys |

## 📖 Example Commands

```bash
# Basic example
python example_basic_workflow.py

# Advanced example
python example_advanced_workflow.py

# CLI - single query
python main_workflow.py "What is machine learning?"

# CLI - interactive
python main_workflow.py

# Show project summary
python PROJECT_SUMMARY.py

# Show this guide
type QUICK_REFERENCE.md
```

## 🔗 Integration Example

```python
# Use in your application
from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

class MyApp:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
    
    async def analyze_query(self, user_query: str) -> str:
        state = WorkflowState(query=user_query)
        result = await self.coordinator.execute(state)
        return result.final_answer

# Usage
app = MyApp()
answer = asyncio.run(app.analyze_query("Your question"))
```

## 📞 Support Resources

- **Setup Guide**: `SETUP_GUIDE.py`
- **File Listing**: `FILE_LISTING.md`
- **Project Summary**: `PROJECT_SUMMARY.py`
- **Examples**: `example_basic_workflow.py`, `example_advanced_workflow.py`
- **Tests**: `test_agents.py`
- **Inline Docs**: All Python files have docstrings

---

**Version**: 1.0  
**Status**: Production Ready  
**Created**: 2024  

For full documentation, see `SETUP_GUIDE.py`
