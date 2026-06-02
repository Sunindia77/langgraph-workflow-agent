"""Researcher agent for information gathering."""
from typing import Any, Dict, Optional
import logging

from base_agent import BaseAgent
from state_schemas import WorkflowState, AgentConfig
from search_tools import SearchToolManager, WebSearchTool, DocumentSearchTool


class ResearcherAgent(BaseAgent):
    """Agent that gathers and organizes information."""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize researcher agent."""
        if config is None:
            config = AgentConfig(
                name="researcher",
                description="Gathers information from multiple sources",
                tools=["web_search", "document_search"]
            )
        
        super().__init__(config)
        self.search_manager = SearchToolManager()
        self._setup_search_tools()
    
    def _setup_search_tools(self) -> None:
        """Setup available search tools."""
        self.search_manager.register_tool(WebSearchTool())
        
        # Example documents
        docs = {
            "doc_1": "Artificial Intelligence is transforming industries...",
            "doc_2": "Machine Learning algorithms can be supervised or unsupervised...",
            "doc_3": "Large Language Models have revolutionized NLP tasks..."
        }
        self.search_manager.register_tool(DocumentSearchTool(docs))
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Execute researcher agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with search results
        """
        self.logger.info(f"Researcher executing for query: {state.query}")
        
        state.current_agent = self.config.name
        
        # Add user message
        state = self.add_message(state, "user", f"Research topic: {state.query}")
        
        try:
            # Execute web search
            self.logger.debug("Executing web search...")
            web_results = await self.call_tool("web_search", query=state.query)
            
            # Execute document search
            self.logger.debug("Executing document search...")
            doc_results = await self.call_tool("document_search", query=state.query)
            
            # Combine results
            all_results = {
                "web_results": web_results,
                "document_results": doc_results
            }
            
            state.search_results = web_results + doc_results if doc_results else web_results
            
            # Add to metadata
            state.metadata["researcher_results"] = all_results
            state.metadata["search_count"] = len(state.search_results)
            
            # Log execution
            self._log_execution(
                "researcher_search",
                "success",
                web_results_count=len(web_results),
                doc_results_count=len(doc_results)
            )
            
            # Add response message
            state = self.add_message(
                state,
                "assistant",
                f"Found {len(state.search_results)} relevant sources"
            )
            
            self.logger.info("Researcher completed successfully")
            
        except Exception as e:
            self.logger.error(f"Researcher error: {str(e)}")
            state = self.add_message(state, "assistant", f"Error during research: {str(e)}")
            self._log_execution("researcher_search", "failed", error=str(e))
        
        return state
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a search tool.
        
        Args:
            tool_name: Name of tool to call
            **kwargs: Tool parameters
            
        Returns:
            Tool result
        """
        self.logger.debug(f"Calling tool: {tool_name} with params: {kwargs}")
        
        try:
            result = await self.search_manager.search(tool_name, **kwargs)
            
            # Record tool call
            state = WorkflowState(query=kwargs.get("query", ""))
            state = self.add_tool_call(
                state,
                tool_name,
                kwargs,
                result,
                status="success"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Tool call failed: {str(e)}")
            raise
