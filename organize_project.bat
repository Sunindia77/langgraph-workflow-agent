@echo off
REM Organize LangGraph project into proper folder structure
REM Run this batch file from the python directory

echo.
echo ================================================================
echo   LangGraph Project Organization Script
echo ================================================================
echo.

REM Create directory structure
echo Creating project directories...
mkdir "langgraph-workflow-agent\src\agents" 2>nul
mkdir "langgraph-workflow-agent\src\tools" 2>nul
mkdir "langgraph-workflow-agent\src\state" 2>nul
mkdir "langgraph-workflow-agent\src\utils" 2>nul
mkdir "langgraph-workflow-agent\examples" 2>nul
mkdir "langgraph-workflow-agent\tests" 2>nul
mkdir "langgraph-workflow-agent\docs" 2>nul

echo.
echo Creating __init__.py files...
type nul > "langgraph-workflow-agent\src\__init__.py"
type nul > "langgraph-workflow-agent\src\agents\__init__.py"
type nul > "langgraph-workflow-agent\src\tools\__init__.py"
type nul > "langgraph-workflow-agent\src\state\__init__.py"
type nul > "langgraph-workflow-agent\src\utils\__init__.py"
type nul > "langgraph-workflow-agent\tests\__init__.py"

echo.
echo Moving Agent files...
copy "base_agent.py" "langgraph-workflow-agent\src\agents\" >nul
copy "researcher_agent.py" "langgraph-workflow-agent\src\agents\" >nul
copy "analyzer_agent.py" "langgraph-workflow-agent\src\agents\" >nul
copy "coordinator_agent.py" "langgraph-workflow-agent\src\agents\" >nul

echo Moving Tool files...
copy "search_tools.py" "langgraph-workflow-agent\src\tools\" >nul
copy "retrieval_tools.py" "langgraph-workflow-agent\src\tools\" >nul
copy "analysis_tools.py" "langgraph-workflow-agent\src\tools\" >nul

echo Moving State and Utils files...
copy "state_schemas.py" "langgraph-workflow-agent\src\state\schemas.py" >nul
copy "env_config.py" "langgraph-workflow-agent\src\utils\llm_config.py" >nul
copy "logging_setup.py" "langgraph-workflow-agent\src\utils\logging.py" >nul

echo Moving Example files...
copy "example_basic_workflow.py" "langgraph-workflow-agent\examples\basic_workflow.py" >nul
copy "example_advanced_workflow.py" "langgraph-workflow-agent\examples\advanced_workflow.py" >nul
copy "main_workflow.py" "langgraph-workflow-agent\examples\main.py" >nul

echo Moving Test files...
copy "test_agents.py" "langgraph-workflow-agent\tests\" >nul

echo Moving Configuration files...
copy "requirements_langgraph.txt" "langgraph-workflow-agent\requirements.txt" >nul
copy ".env.example" "langgraph-workflow-agent\" >nul
copy "pyproject.toml" "langgraph-workflow-agent\" >nul

echo Moving Documentation files...
copy "SETUP_GUIDE.py" "langgraph-workflow-agent\docs\" >nul
copy "QUICK_REFERENCE.md" "langgraph-workflow-agent\docs\" >nul
copy "FILE_LISTING.md" "langgraph-workflow-agent\docs\" >nul
copy "MANIFEST.md" "langgraph-workflow-agent\docs\" >nul
copy "langgraph_agent_README.md" "langgraph-workflow-agent\docs\" >nul
copy "START_HERE.py" "langgraph-workflow-agent\docs\" >nul
copy "PROJECT_SUMMARY.py" "langgraph-workflow-agent\docs\" >nul

echo.
echo ================================================================
echo   Project Organization Complete!
echo ================================================================
echo.
echo Project Location: langgraph-workflow-agent\
echo.
echo Next Steps:
echo   1. cd langgraph-workflow-agent
echo   2. pip install -r requirements.txt
echo   3. copy .env.example .env
echo   4. python examples\basic_workflow.py
echo.
echo ================================================================
pause
