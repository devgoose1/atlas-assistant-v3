"""
Local file search tool for JARVIS

Search and read files from the user's home directory.
"""

from .base import BaseTool, ToolResult
from pathlib import Path
from typing import List, Optional
import mimetypes


class FileSearchTool(BaseTool):
    """Search and read local files."""

    def __init__(self, search_root: Optional[str] = None, max_depth: int = 5):
        super().__init__(
            name="file_search",
            description="Search and read local files from home directory"
        )
        # Restrict to home directory for security
        self.search_root = Path(search_root or Path.home())
        self.max_depth = max_depth
        self.allowed_extensions = {
            '.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml',
            '.html', '.css', '.sql', '.sh', '.c', '.h', '.cpp',
            '.java', '.go', '.rs', '.rb', '.php', '.r', '.m'
        }

    def execute(self, query: str, search_type: str = "filename", max_results: int = 10, **kwargs) -> ToolResult:
        """
        Execute file search.
        
        Args:
            query: Search term
            search_type: "filename" or "content"
            max_results: Maximum results
            
        Returns:
            ToolResult with matching files
        """
        try:
            results = []

            if search_type == "filename":
                results = self._search_by_filename(query, max_results)
            elif search_type == "content":
                results = self._search_by_content(query, max_results)
            else:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Unknown search type: {search_type}"
                )

            if not results:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"No files found matching: {query}"
                )

            # Format context for LLM
            context = f"Found {len(results)} file(s) matching '{query}':\n\n"
            for filepath, preview in results:
                context += f"📄 {filepath}\n"
                if preview:
                    context += f"Preview: {preview[:200]}...\n\n"

            return ToolResult(
                success=True,
                data=results,
                context=context,
                metadata={"query": query, "search_type": search_type, "count": len(results)}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"File search failed: {str(e)}"
            )

    def _search_by_filename(self, query: str, max_results: int) -> List[tuple]:
        """Search files by name."""
        results = []
        query_lower = query.lower()

        try:
            for filepath in self.search_root.rglob("*"):
                if len(results) >= max_results:
                    break

                # Skip directories and hidden files
                if filepath.is_dir() or filepath.name.startswith('.'):
                    continue

                # Check depth
                if filepath.relative_to(self.search_root).parts.__len__() > self.max_depth:
                    continue

                # Check if filename matches
                if query_lower in filepath.name.lower():
                    # Try to read first 200 chars of file
                    preview = self._get_preview(filepath)
                    results.append((str(filepath.relative_to(self.search_root)), preview))
        except PermissionError:
            pass

        return results

    def _search_by_content(self, query: str, max_results: int) -> List[tuple]:
        """Search file contents (text files only)."""
        results = []
        query_lower = query.lower()

        try:
            for filepath in self.search_root.rglob("*"):
                if len(results) >= max_results:
                    break

                if filepath.is_dir() or filepath.name.startswith('.'):
                    continue

                if filepath.suffix not in self.allowed_extensions:
                    continue

                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if query_lower in content.lower():
                            # Find context around match
                            idx = content.lower().find(query_lower)
                            start = max(0, idx - 100)
                            end = min(len(content), idx + 100)
                            preview = f"...{content[start:end]}..."
                            results.append((str(filepath.relative_to(self.search_root)), preview))
                except (UnicodeDecodeError, IOError):
                    pass
        except PermissionError:
            pass

        return results

    def _get_preview(self, filepath: Path, chars: int = 200) -> Optional[str]:
        """Get preview of file content."""
        if filepath.suffix not in self.allowed_extensions:
            return None

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(chars)
        except (IOError, OSError):
            return None

    def is_available(self) -> bool:
        """File search is always available."""
        return True
