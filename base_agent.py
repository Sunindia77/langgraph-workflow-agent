"""Base agent class with LangGraph integration."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import asyncio
import logging

from state_schemas import WorkflowState, ToolCall, Message, AgentConfig


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, config: AgentConfig):
        """
        Initialize agent with configuration.
        
        Args:
            config: AgentConfig with agent settings
        """
        self.config = config
        self.logger = logging.getLogger(f"agent.{config.name}")
        self.execution_history: List[Dict[str, Any]] = []
        
    @abstractmethod
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Execute agent logic.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated workflow state
        """
        pass
    
    @abstractmethod
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a tool and return result.
        
        Args:
            tool_name: Name of tool to call
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        pass
    
    def _log_execution(self, tool_name: str, status: str, **details):
        """Log tool execution for debugging."""
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "status": status,
            "details": details
        }
        self.execution_history.append(execution_record)
        self.logger.info(f"Execution: {tool_name} - {status}")
    
    async def _execute_with_retry(
        self,
        func,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        **kwargs
    ) -> Any:
        """
        Execute function with exponential backoff retry.
        
        Args:
            func: Async function to execute
            max_retries: Maximum number of retries
            backoff_factor: Exponential backoff multiplier
            **kwargs: Function arguments
            
        Returns:
            Function result
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Attempt {attempt + 1}/{max_retries}")
                return await func(**kwargs)
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(f"All {max_retries} attempts failed")
        
        raise last_error
    
    def add_message(self, state: WorkflowState, role: str, content: str) -> WorkflowState:
        """Add message to state."""
        state.messages.append(Message(role=role, content=content))
        return state
    
    def add_tool_call(
        self,
        state: WorkflowState,
        tool_name: str,
        input_params: Dict[str, Any],
        output: Any,
        status: str = "success",
        error: Optional[str] = None
    ) -> WorkflowState:
        """Record tool call in state."""
        tool_call = ToolCall(
            tool_name=tool_name,
            input_params=input_params,
            output=output,
            status=status,
            error=error
        )
        state.tool_calls.append(tool_call)
        return state
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all executions."""
        return {
            "agent": self.config.name,
            "total_calls": len(self.execution_history),
            "history": self.execution_history
        }
