"""
Tool manager for JARVIS

Manages available tools and routes queries to appropriate tools.
"""

from .base import BaseTool, ToolResult
from .web_search import WebSearchTool
from .file_search import FileSearchTool
from .email_tool import EmailTool
from .notes_tool import NotesTool
from .todo_tool import TodoTool
from .calendar_tool import CalendarTool
from .code_tool import CodeTool
from .cad_tool import CADTool
from typing import Dict, List, Optional
import re


class ToolManager:
    """
    Manages JARVIS tools and routes user queries to appropriate tools.
    
    Detects tool usage from natural language queries and executes them.
    """

    def __init__(self):
        """Initialize tool manager with all available tools."""
        self.tools: Dict[str, BaseTool] = {
            "web_search": WebSearchTool(),
            "file_search": FileSearchTool(),
            "email": EmailTool(),
            "notes": NotesTool(),
            "todo": TodoTool(),
            "calendar": CalendarTool(),
            "code": CodeTool(),
            "cad": CADTool(),
        }

        # Tool keywords for detection
        self.tool_keywords = {
            "web_search": ["search", "google", "web", "find", "look up", "what is", "who is", "when"],
            "file_search": ["file", "document", "find file", "search file", "find document"],
            "email": ["email", "mail", "message", "inbox", "unread"],
            "notes": ["note", "remember", "save", "note that", "write down"],
            "todo": ["todo", "task", "add task", "remember to", "need to", "must do"],
            "calendar": ["calendar", "event", "meeting", "schedule", "when is", "what time"],
            "code": ["code", "programming", "debug", "python", "javascript", "refactor", "optimize"],
            "cad": ["circuit", "pcb", "openscad", "3d", "design", "schematic"],
        }

    def detect_tool(self, query: str) -> List[str]:
        """
        Detect which tool(s) might be needed for a query.
        
        Args:
            query: User query text
            
        Returns:
            List of tool names that might be relevant
        """
        query_lower = query.lower()
        detected = []

        for tool_name, keywords in self.tool_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if tool_name not in detected:
                        detected.append(tool_name)
                    break

        return detected

    def execute_tool(self, tool_name: str, query: str, **kwargs) -> ToolResult:
        """
        Execute a specific tool.
        
        Args:
            tool_name: Name of the tool to execute
            query: Query string for the tool
            **kwargs: Additional parameters for the tool
            
        Returns:
            ToolResult with execution results
        """
        if tool_name not in self.tools:
            return ToolResult(
                success=False,
                data=None,
                error=f"Unknown tool: {tool_name}"
            )

        tool = self.tools[tool_name]

        if not tool.is_available():
            return ToolResult(
                success=False,
                data=None,
                error=f"Tool '{tool_name}' is not available"
            )

        return tool.execute(query, **kwargs)

    def get_available_tools(self) -> Dict[str, str]:
        """
        Get list of available tools.
        
        Returns:
            Dictionary of tool names and descriptions
        """
        return {
            name: tool.description
            for name, tool in self.tools.items()
            if tool.is_available()
        }

    def execute_auto(self, query: str, **kwargs) -> Dict:
        """
        Automatically detect and execute relevant tools.
        
        Args:
            query: User query
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with tool results and combined context
        """
        detected_tools = self.detect_tool(query)

        if not detected_tools:
            return {
                "success": False,
                "message": "No tools detected for this query",
                "tools_used": []
            }

        results = {
            "success": True,
            "tools_used": [],
            "results": {},
            "context": ""
        }

        for tool_name in detected_tools:
            result = self.execute_tool(tool_name, query, **kwargs)

            results["tools_used"].append(tool_name)
            results["results"][tool_name] = {
                "success": result.success,
                "data": result.data,
                "error": result.error,
                "metadata": result.metadata
            }

            if result.success and result.context:
                results["context"] += f"\n## {tool_name.replace('_', ' ').title()}\n"
                results["context"] += result.context

        return results
