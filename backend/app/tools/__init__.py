"""
Tool system for JARVIS Assistant

Provides pluggable tools that JARVIS can use to extend its capabilities:
- Web search
- Local file search
- Email checking
- Todo/notes management
- Calendar integration
- Code analysis
- CAD design help
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

__all__ = [
    "BaseTool",
    "ToolResult",
    "WebSearchTool",
    "FileSearchTool",
    "EmailTool",
    "NotesTool",
    "TodoTool",
    "CalendarTool",
    "CodeTool",
    "CADTool",
]
