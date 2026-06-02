# LangGraph Multi-Tool Workflow Agent

A production-ready agentic AI system built with LangGraph, featuring multi-agent orchestration, tool calling, and RAG integration.

## Features

- 🤖 **Multi-Agent Architecture**: Researcher, Analyzer, and Coordinator agents
- 🔧 **Tool Management**: Extensible tool system with search, retrieval, and analysis
- 📊 **RAG Integration**: Built-in retrieval-augmented generation capabilities
- 🔄 **State Management**: Type-safe state handling with Pydantic
- ⚡ **Async Support**: Full async/await implementation
- 🛡️ **Error Handling**: Robust error handling and fallbacks
- 📝 **Structured Logging**: Comprehensive logging throughout
- 🧪 **Production Ready**: Type hints, tests, and examples included

## Quick Start

### Installation

```bash
cd langgraph-workflow-agent
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Set your LLM provider credentials:
   ```bash
   OPENAI_API_KEY=your_key_here
   # or
   ANTHROPIC_API_KEY=your_key_here
   ```

### Basic Usage

```python
from src.agents import CoordinatorAgent
from src.state.schemas import WorkflowState

async def main():
    coordinator = CoordinatorAgent()
    state = WorkflowState(query="Analyze the latest AI trends")
    result = await coordinator.execute(state)
    print(result)
```

## Project Structure

```
src/
├── agents/           # Agent implementations
│   ├── base_agent.py
│   ├── researcher_agent.py
│   ├── analyzer_agent.py
│   └── coordinator_agent.py
├── tools/            # Tool definitions
│   ├── search_tools.py
│   ├── retrieval_tools.py
│   └── analysis_tools.py
├── state/            # State schemas
│   └── schemas.py
├── utils/            # Utilities
│   ├── llm_config.py
│   └── logging.py
└── main.py           # Entry point

tests/               # Unit tests
examples/            # Usage examples
```

## Configuration

### LLM Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude models

### Vector DB

- **Chroma**: In-memory or persistent

## Examples

### Basic Workflow
```bash
python examples/basic_workflow.py
```

### Advanced Multi-Agent
```bash
python examples/advanced_workflow.py
```

## License

MIT
