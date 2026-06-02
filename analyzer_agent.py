"""Analyzer agent for data analysis and synthesis."""
from typing import Any, Dict, Optional
import logging

from base_agent import BaseAgent
from state_schemas import WorkflowState, AgentConfig
from retrieval_tools import VectorStoreRetriever, RAGContext
from analysis_tools import AnalysisToolManager


class AnalyzerAgent(BaseAgent):
    """Agent that analyzes and synthesizes information."""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize analyzer agent."""
        if config is None:
            config = AgentConfig(
                name="analyzer",
                description="Analyzes and synthesizes information",
                tools=["retrieval", "synthesis", "pattern_detection"]
            )
        
        super().__init__(config)
        
        # Initialize RAG components
        self.retriever = VectorStoreRetriever()
        self.rag_context = RAGContext(self.retriever)
        
        # Initialize analysis tools
        self.analysis_manager = AnalysisToolManager()
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Execute analyzer agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with analysis results
        """
        self.logger.info(f"Analyzer executing for query: {state.query}")
        
        state.current_agent = self.config.name
        
        # Add message
        state = self.add_message(state, "user", f"Analyze: {state.query}")
        
        try:
            # Use search results as context
            if state.search_results:
                self.logger.debug("Processing search results...")
                
                # Add search results to retrieval system
                for i, result in enumerate(state.search_results):
                    doc_text = f"{result.get('title', '')} - {result.get('snippet', '')}"
                    await self.retriever.add_document(
                        doc_text,
                        metadata={"source": result.get('url', '')}
                    )
                
                # Retrieve context
                self.logger.debug("Retrieving relevant context...")
                context = await self.rag_context.get_context(state.query, top_k=5)
                state.retrieval_context = context.split("\n---\n")
            
            # Run analysis pipeline
            self.logger.debug("Running analysis pipeline...")
            analysis_result = await self.analysis_manager.pipeline(
                state.search_results,
                ["data_aggregator", "synthesis", "pattern_detector", "validator"]
            )
            
            state.analysis_results = analysis_result
            
            # Log execution
            self._log_execution(
                "analyzer_analysis",
                "success",
                context_size=len(state.retrieval_context),
                analysis_steps=len(analysis_result.get("steps", []))
            )
            
            # Generate summary
            summary = self._generate_summary(analysis_result)
            state = self.add_message(state, "assistant", summary)
            
            self.logger.info("Analyzer completed successfully")
            
        except Exception as e:
            self.logger.error(f"Analyzer error: {str(e)}")
            state = self.add_message(state, "assistant", f"Analysis error: {str(e)}")
            self._log_execution("analyzer_analysis", "failed", error=str(e))
        
        return state
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call an analysis tool.
        
        Args:
            tool_name: Name of tool to call
            **kwargs: Tool parameters
            
        Returns:
            Tool result
        """
        self.logger.debug(f"Calling analysis tool: {tool_name}")
        
        try:
            if tool_name == "retrieval":
                query = kwargs.get("query", "")
                result = await self.rag_context.get_context(query)
            elif tool_name.startswith("analysis_"):
                # Extract actual tool name
                actual_tool = tool_name.replace("analysis_", "")
                data = kwargs.get("data")
                result = await self.analysis_manager.analyze(actual_tool, data, **kwargs)
            else:
                result = await self.analysis_manager.analyze(tool_name, **kwargs)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Analysis tool call failed: {str(e)}")
            raise
    
    def _generate_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Generate human-readable summary."""
        summary_parts = []
        
        # Extract findings from analysis steps
        for step in analysis_result.get("steps", []):
            tool_name = step.get("tool", "unknown")
            result = step.get("result", {})
            
            if tool_name == "synthesis":
                findings = result.get("key_findings", [])
                if findings:
                    summary_parts.append(f"Key Findings: {len(findings)} items identified")
            
            elif tool_name == "pattern_detector":
                patterns = result.get("detected_patterns", [])
                if patterns:
                    summary_parts.append(f"Patterns Detected: {len(patterns)} patterns found")
            
            elif tool_name == "validator":
                status = result.get("status", "unknown")
                score = result.get("score", 0)
                summary_parts.append(f"Data Quality: {status} (score: {score:.2f})")
        
        summary = " | ".join(summary_parts) if summary_parts else "Analysis completed"
        return f"Analysis Summary: {summary}"
