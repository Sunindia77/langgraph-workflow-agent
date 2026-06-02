"""
Script to organize LangGraph project files into proper folder structure.
Run this to move all files into organized directories.
"""

import os
import shutil
from pathlib import Path

def create_project_structure():
    """Create the project folder structure."""
    
    # Define project root
    base_dir = Path(__file__).parent
    project_root = base_dir / "langgraph-workflow-agent"
    
    # Define all directories to create
    directories = [
        project_root / "src" / "agents",
        project_root / "src" / "tools",
        project_root / "src" / "state",
        project_root / "src" / "utils",
        project_root / "examples",
        project_root / "tests",
        project_root / "docs",
    ]
    
    # Create all directories
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")
    
    # Define file movements (source -> destination_folder)
    file_moves = {
        # Agents
        "base_agent.py": project_root / "src" / "agents",
        "researcher_agent.py": project_root / "src" / "agents",
        "analyzer_agent.py": project_root / "src" / "agents",
        "coordinator_agent.py": project_root / "src" / "agents",
        
        # Tools
        "search_tools.py": project_root / "src" / "tools",
        "retrieval_tools.py": project_root / "src" / "tools",
        "analysis_tools.py": project_root / "src" / "tools",
        
        # State
        "state_schemas.py": project_root / "src" / "state" / "schemas.py",
        
        # Utils
        "env_config.py": project_root / "src" / "utils" / "llm_config.py",
        "logging_setup.py": project_root / "src" / "utils" / "logging.py",
        
        # Examples
        "example_basic_workflow.py": project_root / "examples" / "basic_workflow.py",
        "example_advanced_workflow.py": project_root / "examples" / "advanced_workflow.py",
        "main_workflow.py": project_root / "examples" / "main.py",
        
        # Tests
        "test_agents.py": project_root / "tests",
        
        # Config
        "requirements_langgraph.txt": project_root / "requirements.txt",
        ".env.example": project_root,
        "pyproject.toml": project_root,
        
        # Docs
        "SETUP_GUIDE.py": project_root / "docs",
        "QUICK_REFERENCE.md": project_root / "docs",
        "FILE_LISTING.md": project_root / "docs",
        "MANIFEST.md": project_root / "docs",
        "langgraph_agent_README.md": project_root / "docs",
        "START_HERE.py": project_root / "docs",
        "PROJECT_SUMMARY.py": project_root / "docs",
    }
    
    # Create __init__.py files for packages
    init_files = [
        project_root / "src" / "__init__.py",
        project_root / "src" / "agents" / "__init__.py",
        project_root / "src" / "tools" / "__init__.py",
        project_root / "src" / "state" / "__init__.py",
        project_root / "src" / "utils" / "__init__.py",
        project_root / "tests" / "__init__.py",
    ]
    
    print("\n✓ Creating __init__.py files...")
    for init_file in init_files:
        init_file.touch()
        print(f"  Created: {init_file.name}")
    
    # Move files
    print("\n✓ Organizing files...")
    moved_count = 0
    
    for source_name, dest_path in file_moves.items():
        source_file = base_dir / source_name
        
        if not source_file.exists():
            print(f"  ⚠ Skipped (not found): {source_name}")
            continue
        
        # Handle both files and directories
        if isinstance(dest_path, Path) and str(dest_path).endswith(('.py', '.txt', '.toml', '.md')):
            # It's a file with full path including filename
            dest_file = dest_path
        else:
            # It's a directory, keep original filename
            dest_file = dest_path / source_name
        
        # Create destination directory if needed
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file (don't delete original for safety)
        shutil.copy2(source_file, dest_file)
        print(f"  ✓ {source_name:35} → {dest_file.relative_to(base_dir)}")
        moved_count += 1
    
    # Create README
    readme_path = project_root / "README.md"
    if not readme_path.exists():
        readme_content = """# LangGraph Multi-Tool Workflow Agent

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
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Set your LLM provider credentials

### Basic Usage

```python
from src.agents import CoordinatorAgent
from src.state.schemas import WorkflowState

async def main():
    coordinator = CoordinatorAgent()
    state = WorkflowState(query="Your query")
    result = await coordinator.execute(state)
    print(result.final_answer)
```

## Project Structure

```
langgraph-workflow-agent/
├── src/
│   ├── agents/              # Agent implementations
│   ├── tools/               # Tool definitions
│   ├── state/               # State schemas
│   └── utils/               # Utilities
├── examples/                # Example workflows
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## Examples

### Basic Workflow
```bash
python examples/basic_workflow.py
```

### Advanced Multi-Agent
```bash
python examples/advanced_workflow.py
```

### Interactive CLI
```bash
python examples/main.py
```

## Testing

```bash
pytest tests/ -v
```

## Documentation

See `docs/` folder for:
- SETUP_GUIDE.py - Complete setup instructions
- QUICK_REFERENCE.md - Quick lookup guide
- FILE_LISTING.md - File descriptions

## License

MIT
"""
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"\n✓ Created: README.md")
    
    print(f"\n" + "="*70)
    print(f"✅ Project organization complete!")
    print(f"="*70)
    print(f"\n📁 Project location: {project_root}")
    print(f"📦 Files organized: {moved_count}")
    print(f"\n📖 Next steps:")
    print(f"  1. cd langgraph-workflow-agent")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. copy .env.example .env")
    print(f"  4. python examples/basic_workflow.py")
    print(f"\n✨ Your organized LangGraph project is ready!")

if __name__ == "__main__":
    create_project_structure()
