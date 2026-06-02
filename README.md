# 🤖 LangGraph Multi-Agent Workflow System

A sophisticated multi-agent AI system built with LangGraph and Streamlit that orchestrates specialized agents (Researcher, Analyzer, Coordinator) to process complex queries through a 3-phase workflow: Research, Analysis, and Synthesis.

## 🌟 Features

- **🔗 Multi-Agent Orchestration**: Coordinator agent manages workflow between specialized agents
- **🔍 Intelligent Research**: Researcher agent gathers relevant information from multiple sources
- **📊 Advanced Analysis**: Analyzer agent processes and extracts insights from retrieved data
- **🌐 Streamlit Web UI**: Interactive interface for query input and result visualization
- **⚡ Async Processing**: Non-blocking workflow execution with real-time progress tracking
- **💾 State Management**: Pydantic-based state schemas for type-safe data handling
- **🛠️ Tool Integration**: Custom tools for search, retrieval, and analysis

## 📋 Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│      Streamlit Web UI (streamlit_app.py)│
│                                          │
│  ├─ Query Input Interface               │
│  ├─ Real-time Progress Tracking         │
│  ├─ Result Visualization (4 Tabs)       │
│  └─ Query History Management            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│     Main Workflow (main_workflow.py)    │
│                                          │
│  ├─ Interactive & Batch Modes           │
│  ├─ Query Routing                       │
│  └─ Result Display Formatting           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Coordinator Agent (coordinator_agent.py)
│                                          │
│  ├─ Phase 1: RESEARCH                   │
│  ├─ Phase 2: ANALYSIS                   │
│  └─ Phase 3: SYNTHESIS                  │
└────────────────┬────────────────────────┘
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
┌──────────┐ ┌─────────┐ ┌─────────────┐
│Researcher│ │Analyzer │ │Base Agent   │
│Agent     │ │Agent    │ │(Abstract)   │
└──────────┘ └─────────┘ └─────────────┘
      │          │
      └──────────┼──────────┐
                 │          │
                 ▼          ▼
        ┌─────────────────────────┐
        │   Tool Execution Layer  │
        │                         │
        │ ├─ search_tools.py      │
        │ ├─ retrieval_tools.py   │
        │ └─ analysis_tools.py    │
        └─────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Web UI for query input and visualization |
| `main_workflow.py` | Entry point and workflow orchestration |
| `coordinator_agent.py` | Manages 3-phase workflow execution |
| `base_agent.py` | Abstract base class for all agents |
| `researcher_agent.py` | Phase 1 - Information gathering |
| `analyzer_agent.py` | Phase 2 - Data analysis and insights |
| `state_schemas.py` | Pydantic models for type-safe state |
| `search_tools.py` | Search functionality |
| `retrieval_tools.py` | Document retrieval |
| `analysis_tools.py` | Analysis and processing |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key (required)
- Anthropic API Key (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sunindia77/langgraph-workflow-agent.git
   cd langgraph-workflow-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_langgraph.txt
   ```

4. **Setup environment variables**
   ```bash
   copy .env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=sk-...
   # ANTHROPIC_API_KEY=sk-...
   ```

### Usage

#### Interactive Streamlit Web UI
```bash
python -m streamlit run streamlit_app.py
```
Open browser: `http://localhost:8501`

#### Command Line
```bash
# Interactive mode
python main_workflow.py

# Single query
python main_workflow.py "What is machine learning?"
```

## 📊 Workflow Phases

### Phase 1: RESEARCH 🔍
- Researcher agent executes search operations
- Retrieves relevant documents and information
- Collects 10+ sources per query

### Phase 2: ANALYSIS 📊
- Analyzer agent processes retrieved data
- Extracts key insights and patterns
- Generates analysis steps

### Phase 3: SYNTHESIS ✨
- Coordinator aggregates results
- Synthesizes final comprehensive answer
- Combines research and analysis outputs

## 💡 Example Queries

```
✓ "What is machine learning?"
✓ "Explain deep learning and neural networks"
✓ "How does natural language processing work?"
✓ "What are the applications of AI?"
✓ "Describe the transformer architecture"
```

## 📈 Results Display

The Streamlit UI shows results in 4 tabs:

1. **📝 Summary** - Key metrics
   - Sources Processed
   - Messages
   - Analysis Steps
   - Tool Calls

2. **🔍 Details** - Comprehensive breakdown
   - Search Results (expandable)
   - Analysis Results (expandable)
   - Messages (expandable)

3. **📊 Metrics** - Statistical breakdown
   - Numerical metrics
   - Quality indicators

4. **📝 Full Answer** - Complete response
   - Research summary
   - Data quality status
   - Retrieved context

## 🔧 Configuration

Edit `.env` to configure:

```env
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=optional_key
LLM_MODEL=gpt-4

# Vector Database
VECTOR_DB_TYPE=chroma
CHROMA_DB_PATH=./data/chroma

# Agent Settings
AGENT_TIMEOUT=30
MAX_RETRIES=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/workflow.log
```

## 🧪 Testing

Run the test suite:
```bash
python test_agents.py
```

Test individual agents:
```bash
python example_basic_workflow.py
python example_advanced_workflow.py
```

## 📚 Documentation

- [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) - Comprehensive interview preparation
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference guide
- [langgraph_agent_README.md](langgraph_agent_README.md) - Detailed agent documentation
- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) - Architecture deep dive

## 🛠️ Technology Stack

- **LangGraph**: Agent orchestration framework
- **LangChain**: LLM and tool integration
- **Streamlit**: Web UI framework
- **Pydantic**: Data validation and settings
- **Chroma**: Vector database
- **OpenAI**: LLM provider
- **AsyncIO**: Asynchronous execution

## 📦 Dependencies

See `requirements_langgraph.txt` for complete list:
- langchain>=0.1.0
- langgraph>=0.0.10
- pydantic>=2.0
- streamlit>=1.28.0
- openai>=1.0
- anthropic>=0.7
- chromadb>=0.4

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💼 Author

Created by Your Name

## 🆘 Support

For issues and questions:
- Check [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)
- Review example workflows
- Check logs in `./logs/` directory

---

**Ready to get started?** Follow the [Quick Start](#-quick-start) section above!
