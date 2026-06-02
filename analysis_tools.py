"""Analysis tools for data processing and synthesis."""
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import json


class AnalysisTool(ABC):
    """Base class for analysis tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def analyze(self, data: Any, **kwargs) -> Dict[str, Any]:
        """Perform analysis."""
        pass


class DataAggregator(AnalysisTool):
    """Aggregates data from multiple sources."""
    
    def __init__(self):
        super().__init__(
            name="data_aggregator",
            description="Aggregate and combine data from multiple sources"
        )
    
    async def analyze(
        self,
        data: List[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Aggregate data."""
        if not data:
            return {"status": "empty", "count": 0}
        
        aggregation = {
            "total_items": len(data),
            "items": data,
            "summary": {
                "sources": set(),
                "tags": set()
            }
        }
        
        for item in data:
            if "source" in item:
                aggregation["summary"]["sources"].add(item["source"])
            if "tags" in item:
                aggregation["summary"]["tags"].update(item["tags"])
        
        aggregation["summary"]["sources"] = list(aggregation["summary"]["sources"])
        aggregation["summary"]["tags"] = list(aggregation["summary"]["tags"])
        
        return aggregation


class SynthesisTool(AnalysisTool):
    """Synthesizes information from multiple sources."""
    
    def __init__(self):
        super().__init__(
            name="synthesis",
            description="Synthesize and summarize information from multiple sources"
        )
    
    async def analyze(
        self,
        data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Synthesize data."""
        synthesis = {
            "status": "completed",
            "summary": "Data synthesis completed",
            "key_findings": []
        }
        
        # Extract key information
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (str, int, float)):
                    synthesis["key_findings"].append({
                        "aspect": key,
                        "value": str(value)
                    })
                elif isinstance(value, list) and value:
                    synthesis["key_findings"].append({
                        "aspect": key,
                        "value": f"Found {len(value)} items"
                    })
        
        return synthesis


class PatternDetector(AnalysisTool):
    """Detects patterns in data."""
    
    def __init__(self):
        super().__init__(
            name="pattern_detector",
            description="Detect patterns and anomalies in data"
        )
    
    async def analyze(
        self,
        data: List[Dict[str, Any]],
        threshold: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Detect patterns."""
        patterns = {
            "detected_patterns": [],
            "anomalies": [],
            "statistics": {}
        }
        
        if not data:
            return patterns
        
        # Simple pattern detection
        field_values = {}
        for item in data:
            for key, value in item.items():
                if key not in field_values:
                    field_values[key] = []
                field_values[key].append(value)
        
        # Find recurring values
        for field, values in field_values.items():
            value_counts = {}
            for v in values:
                v_str = str(v)
                value_counts[v_str] = value_counts.get(v_str, 0) + 1
            
            total = len(values)
            for value, count in value_counts.items():
                frequency = count / total
                if frequency >= threshold:
                    patterns["detected_patterns"].append({
                        "field": field,
                        "value": value,
                        "frequency": frequency
                    })
        
        patterns["statistics"]["total_items"] = len(data)
        patterns["statistics"]["unique_fields"] = len(field_values)
        
        return patterns


class Validator(AnalysisTool):
    """Validates data quality."""
    
    def __init__(self):
        super().__init__(
            name="validator",
            description="Validate data quality and completeness"
        )
    
    async def analyze(
        self,
        data: Any,
        rules: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Validate data."""
        validation_result = {
            "status": "valid",
            "issues": [],
            "warnings": [],
            "score": 1.0
        }
        
        if not data:
            validation_result["status"] = "invalid"
            validation_result["issues"].append("Data is empty")
            validation_result["score"] = 0.0
            return validation_result
        
        # Basic validation
        if isinstance(data, list):
            if not all(isinstance(item, dict) for item in data):
                validation_result["issues"].append("Not all items are dictionaries")
                validation_result["status"] = "invalid"
                validation_result["score"] -= 0.3
            
            # Check for missing fields
            all_fields = set()
            for item in data:
                all_fields.update(item.keys())
            
            for item in data:
                missing = all_fields - set(item.keys())
                if missing:
                    validation_result["warnings"].append(
                        f"Missing fields: {missing}"
                    )
                    validation_result["score"] -= 0.1
        
        validation_result["score"] = max(0, min(1, validation_result["score"]))
        
        if validation_result["issues"]:
            validation_result["status"] = "invalid"
        elif validation_result["warnings"]:
            validation_result["status"] = "valid_with_warnings"
        
        return validation_result


class AnalysisToolManager:
    """Manages multiple analysis tools."""
    
    def __init__(self):
        self.tools: Dict[str, AnalysisTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self) -> None:
        """Register default analysis tools."""
        self.register_tool(DataAggregator())
        self.register_tool(SynthesisTool())
        self.register_tool(PatternDetector())
        self.register_tool(Validator())
    
    def register_tool(self, tool: AnalysisTool) -> None:
        """Register an analysis tool."""
        self.tools[tool.name] = tool
    
    async def analyze(
        self,
        tool_name: str,
        data: Any,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute analysis with specific tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Analysis tool '{tool_name}' not registered")
        
        return await self.tools[tool_name].analyze(data, **kwargs)
    
    async def pipeline(
        self,
        data: Any,
        tool_sequence: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute multiple analysis tools in sequence."""
        result = data
        results = {"pipeline": tool_sequence, "steps": []}
        
        for tool_name in tool_sequence:
            if tool_name not in self.tools:
                raise ValueError(f"Tool '{tool_name}' not registered")
            
            try:
                step_result = await self.tools[tool_name].analyze(result, **kwargs)
                results["steps"].append({
                    "tool": tool_name,
                    "status": "success",
                    "result": step_result
                })
                result = step_result
            except Exception as e:
                results["steps"].append({
                    "tool": tool_name,
                    "status": "error",
                    "error": str(e)
                })
                break
        
        results["final_result"] = result
        return results
