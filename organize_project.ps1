# LangGraph Project Organization Script
# Run this from the python directory to organize the project

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   LangGraph Project Organization Script" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "langgraph-workflow-agent"
$baseDir = Get-Location

# Create directory structure
Write-Host "Creating project directories..." -ForegroundColor Yellow

$directories = @(
    "$projectRoot\src\agents",
    "$projectRoot\src\tools",
    "$projectRoot\src\state",
    "$projectRoot\src\utils",
    "$projectRoot\examples",
    "$projectRoot\tests",
    "$projectRoot\docs"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "  ✓ $dir" -ForegroundColor Green
}

# Create __init__.py files
Write-Host ""
Write-Host "Creating __init__.py files..." -ForegroundColor Yellow

$initFiles = @(
    "$projectRoot\src\__init__.py",
    "$projectRoot\src\agents\__init__.py",
    "$projectRoot\src\tools\__init__.py",
    "$projectRoot\src\state\__init__.py",
    "$projectRoot\src\utils\__init__.py",
    "$projectRoot\tests\__init__.py"
)

foreach ($file in $initFiles) {
    New-Item -ItemType File -Path $file -Force | Out-Null
    Write-Host "  ✓ $(Split-Path $file -Leaf)" -ForegroundColor Green
}

# Move files
Write-Host ""
Write-Host "Moving files to organized structure..." -ForegroundColor Yellow

# Define file movements
$fileMoves = @{
    # Agents
    "base_agent.py" = "$projectRoot\src\agents\base_agent.py"
    "researcher_agent.py" = "$projectRoot\src\agents\researcher_agent.py"
    "analyzer_agent.py" = "$projectRoot\src\agents\analyzer_agent.py"
    "coordinator_agent.py" = "$projectRoot\src\agents\coordinator_agent.py"
    
    # Tools
    "search_tools.py" = "$projectRoot\src\tools\search_tools.py"
    "retrieval_tools.py" = "$projectRoot\src\tools\retrieval_tools.py"
    "analysis_tools.py" = "$projectRoot\src\tools\analysis_tools.py"
    
    # State
    "state_schemas.py" = "$projectRoot\src\state\schemas.py"
    
    # Utils
    "env_config.py" = "$projectRoot\src\utils\llm_config.py"
    "logging_setup.py" = "$projectRoot\src\utils\logging.py"
    
    # Examples
    "example_basic_workflow.py" = "$projectRoot\examples\basic_workflow.py"
    "example_advanced_workflow.py" = "$projectRoot\examples\advanced_workflow.py"
    "main_workflow.py" = "$projectRoot\examples\main.py"
    
    # Tests
    "test_agents.py" = "$projectRoot\tests\test_agents.py"
    
    # Config
    "requirements_langgraph.txt" = "$projectRoot\requirements.txt"
    ".env.example" = "$projectRoot\.env.example"
    "pyproject.toml" = "$projectRoot\pyproject.toml"
    
    # Docs
    "SETUP_GUIDE.py" = "$projectRoot\docs\SETUP_GUIDE.py"
    "QUICK_REFERENCE.md" = "$projectRoot\docs\QUICK_REFERENCE.md"
    "FILE_LISTING.md" = "$projectRoot\docs\FILE_LISTING.md"
    "MANIFEST.md" = "$projectRoot\docs\MANIFEST.md"
    "langgraph_agent_README.md" = "$projectRoot\docs\langgraph_agent_README.md"
    "START_HERE.py" = "$projectRoot\docs\START_HERE.py"
    "PROJECT_SUMMARY.py" = "$projectRoot\docs\PROJECT_SUMMARY.py"
}

$movedCount = 0

foreach ($source in $fileMoves.Keys) {
    $destination = $fileMoves[$source]
    
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $destination -Force
        Write-Host "  ✓ $source → $(Split-Path $destination)" -ForegroundColor Green
        $movedCount++
    } else {
        Write-Host "  ⚠ Skipped (not found): $source" -ForegroundColor Yellow
    }
}

# Create README
$readmePath = "$projectRoot\README.md"
if (-not (Test-Path $readmePath)) {
    $readmeContent = @"
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

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Configuration

1. Copy \`.env.example\` to \`.env\`
2. Set your LLM provider credentials

### Basic Usage

\`\`\`python
from src.agents import CoordinatorAgent
from src.state.schemas import WorkflowState

async def main():
    coordinator = CoordinatorAgent()
    state = WorkflowState(query="Your query")
    result = await coordinator.execute(state)
    print(result.final_answer)
\`\`\`

## Project Structure

\`\`\`
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
\`\`\`

## Examples

### Basic Workflow
\`\`\`bash
python examples/basic_workflow.py
\`\`\`

### Advanced Multi-Agent
\`\`\`bash
python examples/advanced_workflow.py
\`\`\`

### Interactive CLI
\`\`\`bash
python examples/main.py
\`\`\`

## Testing

\`\`\`bash
pytest tests/ -v
\`\`\`

## Documentation

See \`docs/\` folder for:
- SETUP_GUIDE.py - Complete setup instructions
- QUICK_REFERENCE.md - Quick lookup guide
- FILE_LISTING.md - File descriptions

## License

MIT
"@
    Set-Content -Path $readmePath -Value $readmeContent
    Write-Host "  ✓ Created README.md" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   Project Organization Complete!" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 Project Location: $projectRoot" -ForegroundColor Cyan
Write-Host "📦 Files Organized: $movedCount" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. cd $projectRoot" -ForegroundColor White
Write-Host "  2. pip install -r requirements.txt" -ForegroundColor White
Write-Host "  3. copy .env.example .env" -ForegroundColor White
Write-Host "  4. python examples\basic_workflow.py" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✨ Your organized LangGraph project is ready!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
