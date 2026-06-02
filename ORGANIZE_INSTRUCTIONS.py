"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                  ORGANIZE YOUR LANGGRAPH PROJECT                          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

🎯 WHAT THIS DOES
═══════════════════════════════════════════════════════════════════════════

This will organize all your LangGraph files into a proper project structure:

FROM (Current - All files scattered):
  python/
  ├── base_agent.py
  ├── coordinator_agent.py
  ├── researcher_agent.py
  ├── analyzer_agent.py
  ├── search_tools.py
  ├── retrieval_tools.py
  ├── analysis_tools.py
  ├── state_schemas.py
  ├── ... (and 15+ other files)

TO (Organized - Proper structure):
  python/
  └── langgraph-workflow-agent/
      ├── src/
      │   ├── agents/
      │   │   ├── base_agent.py
      │   │   ├── coordinator_agent.py
      │   │   ├── researcher_agent.py
      │   │   └── analyzer_agent.py
      │   ├── tools/
      │   │   ├── search_tools.py
      │   │   ├── retrieval_tools.py
      │   │   └── analysis_tools.py
      │   ├── state/
      │   │   └── schemas.py
      │   └── utils/
      │       ├── llm_config.py
      │       └── logging.py
      ├── examples/
      │   ├── basic_workflow.py
      │   ├── advanced_workflow.py
      │   └── main.py
      ├── tests/
      │   └── test_agents.py
      ├── docs/
      │   ├── SETUP_GUIDE.py
      │   ├── QUICK_REFERENCE.md
      │   ├── FILE_LISTING.md
      │   └── ... (other docs)
      ├── requirements.txt
      ├── .env.example
      ├── pyproject.toml
      └── README.md

✅ HOW TO RUN
═══════════════════════════════════════════════════════════════════════════

OPTION 1: Windows Batch File (Recommended)
──────────────────────────────────────────
  1. Open Command Prompt (cmd.exe)
  2. Navigate to: c:\Users\HP\OneDrive\Documents\python
  3. Run: organize_project.bat
  4. Press any key when done

OPTION 2: PowerShell
─────────────────────
  1. Open PowerShell
  2. Navigate to: c:\Users\HP\OneDrive\Documents\python
  3. Run: .\organize_project.ps1
  4. Wait for completion message

OPTION 3: Python Script
────────────────────────
  1. Open Command Prompt
  2. Navigate to: c:\Users\HP\OneDrive\Documents\python
  3. Run: python organize_project.py
  4. Wait for completion message

🔧 BEFORE RUNNING
═══════════════════════════════════════════════════════════════════════════

✓ Make sure you're in: c:\Users\HP\OneDrive\Documents\python
✓ Make sure all 24 project files are in this directory
✓ Don't move files manually - let the script do it!

⚠️ NOTES
═══════════════════════════════════════════════════════════════════════════

• The scripts COPY files (don't delete originals) - you can clean up later
• Original files remain in python/ directory for safety
• If organization fails, all files are still safe
• You can run the script multiple times safely

📋 WHAT GETS MOVED
═══════════════════════════════════════════════════════════════════════════

Agents (4 files) → src/agents/
  • base_agent.py
  • coordinator_agent.py
  • researcher_agent.py
  • analyzer_agent.py

Tools (3 files) → src/tools/
  • search_tools.py
  • retrieval_tools.py
  • analysis_tools.py

State & Utils (2 files) → src/state/ & src/utils/
  • state_schemas.py → src/state/schemas.py
  • env_config.py → src/utils/llm_config.py
  • logging_setup.py → src/utils/logging.py

Examples (3 files) → examples/
  • example_basic_workflow.py → basic_workflow.py
  • example_advanced_workflow.py → advanced_workflow.py
  • main_workflow.py → main.py

Tests (1 file) → tests/
  • test_agents.py

Config (3 files) → project root/
  • requirements_langgraph.txt → requirements.txt
  • .env.example
  • pyproject.toml

Docs (7 files) → docs/
  • SETUP_GUIDE.py
  • QUICK_REFERENCE.md
  • FILE_LISTING.md
  • MANIFEST.md
  • langgraph_agent_README.md
  • START_HERE.py
  • PROJECT_SUMMARY.py

✨ AFTER RUNNING
═══════════════════════════════════════════════════════════════════════════

1. You'll have: langgraph-workflow-agent/
2. Project is fully organized
3. Ready to use immediately:
   
   cd langgraph-workflow-agent
   pip install -r requirements.txt
   copy .env.example .env
   python examples/basic_workflow.py

📝 DETAILED STEPS (Manual Alternative)
═══════════════════════════════════════════════════════════════════════════

If you prefer to organize manually:

1. Create folders:
   mkdir langgraph-workflow-agent\src\agents
   mkdir langgraph-workflow-agent\src\tools
   mkdir langgraph-workflow-agent\src\state
   mkdir langgraph-workflow-agent\src\utils
   mkdir langgraph-workflow-agent\examples
   mkdir langgraph-workflow-agent\tests
   mkdir langgraph-workflow-agent\docs

2. Move agent files to: langgraph-workflow-agent\src\agents\
   base_agent.py
   coordinator_agent.py
   researcher_agent.py
   analyzer_agent.py

3. Move tool files to: langgraph-workflow-agent\src\tools\
   search_tools.py
   retrieval_tools.py
   analysis_tools.py

4. Move state files to: langgraph-workflow-agent\src\state\
   state_schemas.py (rename to schemas.py)

5. Move util files to: langgraph-workflow-agent\src\utils\
   env_config.py (rename to llm_config.py)
   logging_setup.py (rename to logging.py)

6. Move examples to: langgraph-workflow-agent\examples\
   example_basic_workflow.py (rename to basic_workflow.py)
   example_advanced_workflow.py (rename to advanced_workflow.py)
   main_workflow.py (rename to main.py)

7. Move tests to: langgraph-workflow-agent\tests\
   test_agents.py

8. Move config to: langgraph-workflow-agent\
   requirements_langgraph.txt (rename to requirements.txt)
   .env.example
   pyproject.toml

9. Move docs to: langgraph-workflow-agent\docs\
   All documentation files

🆘 TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

Issue: "Parent directory does not exist"
Solution: Run the script from c:\Users\HP\OneDrive\Documents\python

Issue: "Permission denied"
Solution: Make sure no files are open in editors, close them first

Issue: Files not found
Solution: Make sure you're running from the correct directory

Issue: Script doesn't run
Solution: Try the Python version (organize_project.py) instead

❓ QUESTIONS?
═══════════════════════════════════════════════════════════════════════════

After organizing:
1. See: langgraph-workflow-agent/docs/START_HERE.py
2. See: langgraph-workflow-agent/docs/QUICK_REFERENCE.md
3. See: langgraph-workflow-agent/README.md

═══════════════════════════════════════════════════════════════════════════

READY TO ORGANIZE?

Choose your method:
  Windows:   organize_project.bat
  PowerShell: organize_project.ps1
  Python:    python organize_project.py

═══════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(__doc__)
