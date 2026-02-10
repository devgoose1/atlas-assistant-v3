"""
Web search tool for JARVIS

Uses DuckDuckGo for privacy-respecting web searches.
"""

from .base import BaseTool, ToolResult
from typing import Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class WebSearchTool(BaseTool):
    """Search the web using DuckDuckGo API."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for current information"
        )

    def execute(self, query: str, max_results: int = 5, **kwargs) -> ToolResult:
        """
        Execute web search.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            ToolResult with search results
        """
        if not self.is_available():
            return ToolResult(
                success=False,
                data=None,
                error="Web search tool not available (requests library required)"
            )

        try:
            # DuckDuckGo API endpoint (simple GET request)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_redirect": 1,
                "no_html": 1,
                "t": "jarvis_assistant"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract results
            results = []
            
            # Abstract (instant answer)
            if data.get("Abstract"):
                results.append({
                    "type": "abstract",
                    "title": query,
                    "content": data["Abstract"],
                    "url": data.get("AbstractURL", "")
                })

            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if "Text" in topic:
                    results.append({
                        "type": "related",
                        "title": topic.get("FirstURL", "").split("/")[-1],
                        "content": topic["Text"],
                        "url": topic.get("FirstURL", "")
                    })

            if not results:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"No results found for: {query}"
                )

            # Format context for LLM
            context = f"Web search results for '{query}':\n\n"
            for i, result in enumerate(results[:max_results], 1):
                context += f"{i}. {result['title']}\n"
                context += f"   {result['content']}\n"
                if result['url']:
                    context += f"   URL: {result['url']}\n\n"

            return ToolResult(
                success=True,
                data=results,
                context=context,
                metadata={"query": query, "count": len(results)}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Web search failed: {str(e)}"
            )

    def is_available(self) -> bool:
        """Check if web search is available."""
        return HAS_REQUESTS
