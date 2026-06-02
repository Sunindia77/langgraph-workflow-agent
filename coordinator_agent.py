"""Coordinator agent for multi-agent orchestration."""
from typing import Optional, Dict, Any, List
import logging
from enum import Enum

from base_agent import BaseAgent
from state_schemas import WorkflowState, AgentConfig
from researcher_agent import ResearcherAgent
from analyzer_agent import AnalyzerAgent


class WorkflowPhase(Enum):
    """Workflow execution phases."""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    COMPLETE = "complete"


class CoordinatorAgent(BaseAgent):
    """Agent that coordinates multiple specialized agents."""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize coordinator agent."""
        if config is None:
            config = AgentConfig(
                name="coordinator",
                description="Coordinates multi-agent workflow",
                tools=["researcher", "analyzer"]
            )
        
        super().__init__(config)
        
        # Initialize sub-agents
        self.researcher = ResearcherAgent()
        self.analyzer = AnalyzerAgent()
        
        self.current_phase = WorkflowPhase.RESEARCH
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Execute coordinator orchestration.
        
        Args:
            state: Current workflow state
            
        Returns:
            Final workflow state with results
        """
        self.logger.info(f"Coordinator starting workflow for query: {state.query}")
        
        state.current_agent = self.config.name
        state = self.add_message(
            state,
            "assistant",
            f"Starting multi-agent workflow for: {state.query}"
        )
        
        try:
            # Phase 1: Research
            self.logger.info("Phase 1: RESEARCH - Gathering information...")
            self.current_phase = WorkflowPhase.RESEARCH
            state = await self._execute_research_phase(state)
            
            # Phase 2: Analysis
            if state.search_results:
                self.logger.info("Phase 2: ANALYSIS - Analyzing information...")
                self.current_phase = WorkflowPhase.ANALYSIS
                state = await self._execute_analysis_phase(state)
            else:
                self.logger.warning("No research results, skipping analysis")
                state = self.add_message(
                    state,
                    "assistant",
                    "No results found to analyze"
                )
            
            # Phase 3: Synthesis
            self.logger.info("Phase 3: SYNTHESIS - Synthesizing results...")
            self.current_phase = WorkflowPhase.SYNTHESIS
            state = await self._execute_synthesis_phase(state)
            
            # Complete
            self.current_phase = WorkflowPhase.COMPLETE
            state = self.add_message(
                state,
                "assistant",
                "Workflow completed successfully"
            )
            
            self.logger.info("Coordinator workflow completed")
            
        except Exception as e:
            self.logger.error(f"Coordinator error: {str(e)}")
            state = self.add_message(state, "assistant", f"Workflow error: {str(e)}")
            self._log_execution("coordinator_workflow", "failed", error=str(e))
        
        return state
    
    async def _execute_research_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute research phase."""
        try:
            state = await self.researcher.execute(state)
            self._log_execution("research_phase", "success")
            return state
        except Exception as e:
            self.logger.error(f"Research phase failed: {str(e)}")
            self._log_execution("research_phase", "failed", error=str(e))
            raise
    
    async def _execute_analysis_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute analysis phase."""
        try:
            state = await self.analyzer.execute(state)
            self._log_execution("analysis_phase", "success")
            return state
        except Exception as e:
            self.logger.error(f"Analysis phase failed: {str(e)}")
            self._log_execution("analysis_phase", "failed", error=str(e))
            raise
    
    async def _execute_synthesis_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute synthesis phase to create final answer."""
        try:
            final_answer = self._synthesize_results(state)
            state.final_answer = final_answer
            
            state = self.add_message(state, "assistant", final_answer)
            
            self._log_execution("synthesis_phase", "success")
            return state
        except Exception as e:
            self.logger.error(f"Synthesis phase failed: {str(e)}")
            self._log_execution("synthesis_phase", "failed", error=str(e))
            raise
    
    def _synthesize_results(self, state: WorkflowState) -> str:
        """Create final synthesized answer."""
        synthesis_parts = []
        
        # Add research summary
        if state.search_results:
            synthesis_parts.append(
                f"**Research Summary:** Found {len(state.search_results)} relevant sources"
            )
        
        # Add analysis insights
        if state.analysis_results:
            final_result = state.analysis_results.get("final_result", {})
            
            if isinstance(final_result, dict):
                validation_status = final_result.get("status", "unknown")
                synthesis_parts.append(
                    f"**Data Quality:** {validation_status}"
                )
        
        # Add retrieval context summary
        if state.retrieval_context:
            synthesis_parts.append(
                f"**Retrieved Context:** {len(state.retrieval_context)} relevant documents"
            )
        
        # Add tool call summary
        if state.tool_calls:
            successful_calls = sum(1 for tc in state.tool_calls if tc.status == "success")
            synthesis_parts.append(
                f"**Tools Executed:** {successful_calls}/{len(state.tool_calls)} successful"
            )
        
        final_answer = "\n\n".join(synthesis_parts) if synthesis_parts else \
                      "Analysis completed with no specific findings"
        
        return final_answer
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a sub-agent.
        
        Args:
            tool_name: Name of agent to call
            **kwargs: Parameters
            
        Returns:
            Result from agent
        """
        self.logger.debug(f"Coordinator calling tool: {tool_name}")
        
        state = kwargs.get("state", WorkflowState(query=""))
        
        if tool_name == "researcher":
            return await self.researcher.execute(state)
        elif tool_name == "analyzer":
            return await self.analyzer.execute(state)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status."""
        return {
            "current_phase": self.current_phase.value,
            "coordinator_executions": self.get_execution_summary(),
            "researcher_executions": self.researcher.get_execution_summary(),
            "analyzer_executions": self.analyzer.get_execution_summary()
        }
