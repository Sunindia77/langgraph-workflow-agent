"""Pydantic state schemas for workflow."""
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Single message in workflow."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ToolCall(BaseModel):
    """Tool execution record."""
    tool_name: str
    input_params: Dict[str, Any]
    output: Any
    status: str  # "success", "failed", "pending"
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class WorkflowState(BaseModel):
    """Main workflow state."""
    query: str
    messages: List[Message] = Field(default_factory=list)
    tool_calls: List[ToolCall] = Field(default_factory=list)
    current_agent: Optional[str] = None
    search_results: List[Dict[str, Any]] = Field(default_factory=list)
    analysis_results: Dict[str, Any] = Field(default_factory=dict)
    retrieval_context: List[str] = Field(default_factory=list)
    final_answer: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True


class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str
    description: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    tools: List[str] = Field(default_factory=list)
    system_prompt: Optional[str] = None
    timeout: int = 30


class ToolDefinition(BaseModel):
    """Definition of a tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    category: str  # "search", "retrieval", "analysis"
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
