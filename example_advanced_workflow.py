"""Advanced workflow example with multiple queries."""
import asyncio
import logging
from typing import List

from coordinator_agent import CoordinatorAgent
from state_schemas import WorkflowState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_query(coordinator: CoordinatorAgent, query: str) -> WorkflowState:
    """Run a single query through the workflow."""
    logger.info(f"\n{'─' * 60}")
    logger.info(f"Processing: {query}")
    logger.info(f"{'─' * 60}")
    
    state = WorkflowState(query=query)
    result = await coordinator.execute(state)
    
    return result


async def main():
    """Run advanced multi-query workflow."""
    logger.info("=" * 60)
    logger.info("LangGraph Multi-Agent Workflow - Advanced Example")
    logger.info("Multiple Concurrent Queries with Detailed Analysis")
    logger.info("=" * 60)
    
    coordinator = CoordinatorAgent()
    
    # Multiple queries to process
    queries = [
        "Latest developments in natural language processing",
        "How are enterprises using machine learning in 2024?",
        "Future of AI safety and alignment research"
    ]
    
    results: List[WorkflowState] = []
    
    # Process queries (you can also run them concurrently with gather)
    for query in queries:
        result = await run_query(coordinator, query)
        results.append(result)
    
    # Display comprehensive results
    logger.info("\n" + "=" * 60)
    logger.info("WORKFLOW SUMMARY")
    logger.info("=" * 60)
    
    for idx, result in enumerate(results, 1):
        logger.info(f"\n📌 Query {idx}: {result.query}")
        
        # Search metrics
        logger.info(f"   Search Results: {len(result.search_results)} found")
        
        # Analysis metrics
        if result.analysis_results:
            steps = result.analysis_results.get("steps", [])
            successful = sum(1 for s in steps if s.get("status") == "success")
            logger.info(f"   Analysis Steps: {successful}/{len(steps)} successful")
        
        # Tool calls
        logger.info(f"   Tool Calls: {len(result.tool_calls)} executed")
        
        # Final answer preview
        if result.final_answer:
            preview = result.final_answer[:100] + "..." \
                     if len(result.final_answer) > 100 else result.final_answer
            logger.info(f"   Result: {preview}")
    
    # Cross-query analysis
    logger.info(f"\n📊 Cross-Query Analysis:")
    total_searches = sum(len(r.search_results) for r in results)
    total_tools = sum(len(r.tool_calls) for r in results)
    avg_messages = sum(len(r.messages) for r in results) / len(results)
    
    logger.info(f"  Total Searches: {total_searches}")
    logger.info(f"  Total Tool Calls: {total_tools}")
    logger.info(f"  Avg Messages per Query: {avg_messages:.1f}")
    
    # Workflow status from coordinator
    status = coordinator.get_workflow_status()
    logger.info(f"\n📋 Coordinator Statistics:")
    logger.info(f"  Phase: {status['current_phase']}")
    logger.info(f"  Total Executions: {status['coordinator_executions']['total_calls']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Advanced workflow completed!")
    logger.info("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
