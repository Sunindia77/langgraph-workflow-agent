"""Search tools for information gathering."""
from typing import Dict, List, Any, Optional
import asyncio
import aiohttp
from abc import ABC, abstractmethod


class SearchTool(ABC):
    """Base class for search tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Execute search."""
        pass


class WebSearchTool(SearchTool):
    """Web search tool using public APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="web_search",
            description="Search the web for information"
        )
        self.api_key = api_key
    
    async def search(
        self,
        query: str,
        max_results: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search the web.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            List of search results
        """
        try:
            # Simulated search results
            results = [
                {
                    "title": f"Result {i+1}: {query}",
                    "url": f"https://example{i}.com/result",
                    "snippet": f"Information about {query} from source {i+1}",
                    "relevance": 1.0 - (i * 0.1)
                }
                for i in range(min(max_results, 10))
            ]
            return results
        except Exception as e:
            raise RuntimeError(f"Search failed: {str(e)}")


class DocumentSearchTool(SearchTool):
    """Search tool for internal documents."""
    
    def __init__(self, documents: Optional[Dict[str, str]] = None):
        super().__init__(
            name="document_search",
            description="Search internal documents and knowledge base"
        )
        self.documents = documents or {}
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search documents.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            Matching documents
        """
        results = []
        query_lower = query.lower()
        
        for doc_id, content in self.documents.items():
            if query_lower in content.lower():
                relevance = content.lower().count(query_lower) / len(content.split())
                results.append({
                    "doc_id": doc_id,
                    "content": content[:500],
                    "relevance": relevance
                })
        
        return sorted(
            results,
            key=lambda x: x["relevance"],
            reverse=True
        )[:max_results]


class APISearchTool(SearchTool):
    """Tool for querying external APIs."""
    
    def __init__(self, endpoint: str, api_key: Optional[str] = None):
        super().__init__(
            name="api_search",
            description="Query external APIs for data"
        )
        self.endpoint = endpoint
        self.api_key = api_key
    
    async def search(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Call external API.
        
        Args:
            query: Query parameter
            params: Additional parameters
            
        Returns:
            API response data
        """
        try:
            request_params = params or {}
            request_params["q"] = query
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.endpoint,
                    params=request_params,
                    headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        raise RuntimeError(f"API error: {response.status}")
        except Exception as e:
            raise RuntimeError(f"API search failed: {str(e)}")


class SearchToolManager:
    """Manages multiple search tools."""
    
    def __init__(self):
        self.tools: Dict[str, SearchTool] = {}
    
    def register_tool(self, tool: SearchTool) -> None:
        """Register a search tool."""
        self.tools[tool.name] = tool
    
    async def search(
        self,
        tool_name: str,
        query: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Execute search with specific tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not registered")
        
        return await self.tools[tool_name].search(query, **kwargs)
    
    async def parallel_search(
        self,
        query: str,
        tool_names: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Execute multiple searches in parallel."""
        tools_to_use = tool_names or list(self.tools.keys())
        
        tasks = [
            self.search(tool_name, query, **kwargs)
            for tool_name in tools_to_use
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            tool_name: result
            for tool_name, result in zip(tools_to_use, results)
            if not isinstance(result, Exception)
        }
