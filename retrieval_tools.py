"""Retrieval and RAG tools for LangGraph agents."""
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod
import json


class RetrieverTool(ABC):
    """Base class for retrieval tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents."""
        pass
    
    @abstractmethod
    async def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add document to retriever."""
        pass


class VectorStoreRetriever(RetrieverTool):
    """Retriever using vector similarity search."""
    
    def __init__(self, name: str = "vector_store"):
        super().__init__(
            name=name,
            description="Retrieve documents using vector similarity"
        )
        self.documents: Dict[str, Tuple[str, Dict[str, Any]]] = {}
        self.embeddings: Dict[str, List[float]] = {}
    
    def _simple_embedding(self, text: str) -> List[float]:
        """Create simple embedding (in production, use real embeddings)."""
        # Simulate embedding by using character frequencies
        embedding = [0.0] * 128
        for i, char in enumerate(text[:512]):
            embedding[i % 128] += ord(char) / 256.0
        
        # Normalize
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        return embedding
    
    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """Compute cosine similarity."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        return dot_product
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Retrieve similar documents."""
        if not self.documents:
            return []
        
        query_embedding = self._simple_embedding(query)
        
        similarities = {}
        for doc_id, (text, metadata) in self.documents.items():
            similarity = self._cosine_similarity(
                query_embedding,
                self.embeddings[doc_id]
            )
            similarities[doc_id] = (similarity, text, metadata)
        
        # Sort by similarity
        sorted_docs = sorted(
            similarities.items(),
            key=lambda x: x[1][0],
            reverse=True
        )
        
        return [
            {
                "doc_id": doc_id,
                "content": text,
                "similarity": score,
                "metadata": metadata
            }
            for doc_id, (score, text, metadata) in sorted_docs[:top_k]
        ]
    
    async def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add document to vector store."""
        doc_id = f"doc_{len(self.documents)}"
        self.documents[doc_id] = (document, metadata or {})
        self.embeddings[doc_id] = self._simple_embedding(document)
        return doc_id


class HybridRetriever(RetrieverTool):
    """Combines multiple retrieval strategies."""
    
    def __init__(self, retrievers: Optional[Dict[str, RetrieverTool]] = None):
        super().__init__(
            name="hybrid_retriever",
            description="Hybrid retrieval combining multiple strategies"
        )
        self.retrievers = retrievers or {}
    
    def add_retriever(self, retriever: RetrieverTool, weight: float = 1.0) -> None:
        """Add retriever with weight."""
        self.retrievers[retriever.name] = (retriever, weight)
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Retrieve using all registered retrievers."""
        all_results = {}
        total_weight = 0.0
        
        for retriever_name, (retriever, weight) in self.retrievers.items():
            try:
                results = await retriever.retrieve(query, top_k=top_k, **kwargs)
                
                for i, result in enumerate(results):
                    doc_id = result.get("doc_id", result.get("id"))
                    score = result.get("similarity", 1.0 - i * 0.1)
                    weighted_score = score * weight
                    
                    if doc_id not in all_results:
                        all_results[doc_id] = {
                            "content": result.get("content", ""),
                            "score": 0.0,
                            "sources": []
                        }
                    
                    all_results[doc_id]["score"] += weighted_score
                    all_results[doc_id]["sources"].append(retriever_name)
                
                total_weight += weight
            except Exception as e:
                print(f"Retriever {retriever_name} failed: {str(e)}")
        
        # Normalize scores and sort
        sorted_results = sorted(
            [
                {
                    "doc_id": doc_id,
                    **data,
                    "normalized_score": data["score"] / total_weight if total_weight > 0 else 0
                }
                for doc_id, data in all_results.items()
            ],
            key=lambda x: x["normalized_score"],
            reverse=True
        )
        
        return sorted_results[:top_k]
    
    async def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add document to all retrievers."""
        ids = []
        for retriever in self.retrievers.values():
            doc_id = await retriever[0].add_document(document, metadata)
            ids.append(doc_id)
        return ids[0] if ids else None


class RAGContext:
    """Manages context for Retrieval-Augmented Generation."""
    
    def __init__(self, retriever: RetrieverTool):
        self.retriever = retriever
        self.context_cache: Dict[str, List[Dict[str, Any]]] = {}
    
    async def get_context(
        self,
        query: str,
        top_k: int = 5,
        use_cache: bool = True
    ) -> str:
        """Get formatted context for LLM."""
        cache_key = f"{query}_{top_k}"
        
        if use_cache and cache_key in self.context_cache:
            documents = self.context_cache[cache_key]
        else:
            documents = await self.retriever.retrieve(query, top_k=top_k)
            if use_cache:
                self.context_cache[cache_key] = documents
        
        # Format context for LLM
        context_parts = []
        for doc in documents:
            context_parts.append(
                f"Source: {doc.get('doc_id', 'unknown')}\n"
                f"Content: {doc.get('content', '')}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    async def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add document and clear cache."""
        self.context_cache.clear()
        return await self.retriever.add_document(document, metadata)
