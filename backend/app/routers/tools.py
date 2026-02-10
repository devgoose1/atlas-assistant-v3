"""
Tools router for JARVIS

API endpoints for tool management and execution.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.tools.manager import ToolManager

router = APIRouter(prefix="/api/tools", tags=["tools"])

# Initialize tool manager
tool_manager = ToolManager()


class ToolRequest(BaseModel):
    """Request to execute a tool."""
    query: str
    tool_name: Optional[str] = None
    action: Optional[str] = None

    model_config = {"extra": "allow"}


class ToolResponse(BaseModel):
    """Response from tool execution."""
    success: bool
    tool: str
    data: Any
    context: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None


@router.get("/available")
async def get_available_tools():
    """Get list of available tools."""
    tools = tool_manager.get_available_tools()
    return {
        "available_tools": tools,
        "tool_count": len(tools)
    }


@router.post("/execute")
async def execute_tool(request: dict):
    """
    Execute a specific tool.
    
    Request:
    {
        "tool": "web_search",
        "query": "what is python",
        "max_results": 5
    }
    """
    tool_name = request.get("tool")
    query = request.get("query")

    if not tool_name or not query:
        raise HTTPException(
            status_code=400,
            detail="Missing required fields: 'tool' and 'query'"
        )

    # Extract tool-specific parameters
    tool_params = {k: v for k, v in request.items() if k not in ["tool", "query"]}

    result = tool_manager.execute_tool(tool_name, query, **tool_params)

    return ToolResponse(
        success=result.success,
        tool=tool_name,
        data=result.data,
        context=result.context,
        error=result.error,
        metadata=result.metadata
    ).model_dump()


@router.post("/auto")
async def execute_auto(request: dict):
    """
    Auto-detect and execute relevant tools.
    
    Request:
    {
        "query": "search for python web frameworks and check my todo list"
    }
    """
    query = request.get("query")

    if not query:
        raise HTTPException(status_code=400, detail="Missing required field: 'query'")

    results = tool_manager.execute_auto(query)

    return results


@router.get("/detect/{query}")
async def detect_tools(query: str):
    """Detect which tools are relevant for a query."""
    detected = tool_manager.detect_tool(query)

    return {
        "query": query,
        "detected_tools": detected,
        "tool_count": len(detected)
    }
