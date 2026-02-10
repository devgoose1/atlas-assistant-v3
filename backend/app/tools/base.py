"""
Base Tool abstraction for JARVIS

All tools inherit from BaseTool and must implement execute().
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class ToolResult:
    """Standard result format from tools."""
    success: bool
    data: Any
    error: Optional[str] = None
    context: Optional[str] = None  # For including in LLM context
    metadata: Optional[Dict[str, Any]] = None


class BaseTool(ABC):
    """
    Abstract base class for all JARVIS tools.
    
    Each tool provides a specific capability (search, email, etc.)
    and returns results in a standardized format.
    """

    def __init__(self, name: str, description: str):
        """
        Initialize tool.
        
        Args:
            name: Tool identifier (e.g., "web_search")
            description: Human-readable description
        """
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, query: str, **kwargs) -> ToolResult:
        """
        Execute the tool with given query/parameters.
        
        Args:
            query: Main input query
            **kwargs: Tool-specific parameters
            
        Returns:
            ToolResult with success status, data, and optional context
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if tool is available (dependencies installed, credentials set, etc.)
        
        Returns:
            True if tool can be used, False otherwise
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
