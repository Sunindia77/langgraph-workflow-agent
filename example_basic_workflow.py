"""Basic workflow example."""
import asyncio
import logging

from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run basic workflow."""
    logger.info("=" * 60)
    logger.info("LangGraph Multi-Agent Workflow - Basic Example")
    logger.info("=" * 60)
    
    # Initialize coordinator
    coordinator = CoordinatorAgent()
    
    # Create initial state
    state = WorkflowState(
        query="What are the latest trends in AI and machine learning?",
        metadata={"example": "basic_workflow"}
    )
    
    logger.info(f"\nQuery: {state.query}\n")
    
    # Execute workflow
    result_state = await coordinator.execute(state)
    
    # Display results
    logger.info("\n" + "=" * 60)
    logger.info("WORKFLOW RESULTS")
    logger.info("=" * 60)
    
    # Messages
    logger.info("\n📝 Messages:")
    for msg in result_state.messages:
        logger.info(f"  [{msg.role.upper()}] {msg.content}")
    
    # Search results
    if result_state.search_results:
        logger.info(f"\n🔍 Search Results ({len(result_state.search_results)} found):")
        for i, result in enumerate(result_state.search_results[:3], 1):
            logger.info(f"  {i}. {result.get('title', 'N/A')}")
            logger.info(f"     URL: {result.get('url', 'N/A')}")
    
    # Analysis results
    if result_state.analysis_results:
        logger.info(f"\n📊 Analysis Results:")
        steps = result_state.analysis_results.get("steps", [])
        for step in steps:
            logger.info(f"  - {step.get('tool', 'unknown')}: {step.get('status', 'unknown')}")
    
    # Final answer
    if result_state.final_answer:
        logger.info(f"\n✅ Final Answer:")
        logger.info(result_state.final_answer)
    
    # Tool calls summary
    if result_state.tool_calls:
        logger.info(f"\n🛠️  Tool Calls ({len(result_state.tool_calls)} total):")
        for tc in result_state.tool_calls:
            logger.info(
                f"  - {tc.tool_name}: {tc.status} "
                f"({len(tc.output) if isinstance(tc.output, list) else 'N/A'} results)"
            )
    
    # Workflow status
    logger.info(f"\n📋 Workflow Status:")
    status = coordinator.get_workflow_status()
    logger.info(f"  Current Phase: {status['current_phase']}")
    logger.info(
        f"  Coordinator Calls: {status['coordinator_executions']['total_calls']}"
    )
    
    logger.info("\n" + "=" * 60)
    logger.info("Workflow completed successfully!")
    logger.info("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
