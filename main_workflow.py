"""Main entry point for LangGraph workflow agent."""
import asyncio
import logging
import sys
from typing import Optional

from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


async def run_workflow(query: str) -> None:
    """
    Run a complete workflow for a given query.
    
    Args:
        query: The user query to process
    """
    logger.info(f"Starting workflow for query: {query}")
    
    # Initialize coordinator
    coordinator = CoordinatorAgent()
    
    # Create initial state
    state = WorkflowState(query=query)
    
    # Execute workflow
    result = await coordinator.execute(state)
    
    # Display results
    print("\n" + "=" * 70)
    print("WORKFLOW RESULTS")
    print("=" * 70)
    
    print(f"\n📌 Query: {result.query}")
    print(f"📝 Messages: {len(result.messages)}")
    print(f"🔍 Search Results: {len(result.search_results)}")
    print(f"📊 Analysis Steps: {len(result.analysis_results.get('steps', []))}")
    print(f"🛠️  Tool Calls: {len(result.tool_calls)}")
    
    if result.final_answer:
        print(f"\n✅ Final Answer:\n{result.final_answer}")
    
    print("\n" + "=" * 70 + "\n")


async def interactive_mode() -> None:
    """Run in interactive mode."""
    print("\n" + "=" * 70)
    print("LangGraph Multi-Agent Workflow System")
    print("=" * 70)
    print("\nEnter queries to analyze (type 'quit' to exit):\n")
    
    coordinator = CoordinatorAgent()
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() == "quit":
                print("Exiting...")
                break
            
            if not query:
                print("Please enter a valid query.\n")
                continue
            
            # Execute workflow
            state = WorkflowState(query=query)
            result = await coordinator.execute(state)
            
            # Display brief results
            print(f"\n✅ Processed {len(result.search_results)} sources")
            if result.final_answer:
                answer_preview = result.final_answer[:200] + "..." \
                               if len(result.final_answer) > 200 else result.final_answer
                print(f"Result: {answer_preview}")
            print()
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            print(f"Error: {str(e)}\n")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Run with provided query
        query = " ".join(sys.argv[1:])
        asyncio.run(run_workflow(query))
    else:
        # Interactive mode
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
