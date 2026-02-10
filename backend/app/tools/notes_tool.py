"""
Notes tool for JARVIS

Create, read, and search personal notes/knowledge base.
"""

from .base import BaseTool, ToolResult
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


class NotesTool(BaseTool):
    """Manage and search notes."""

    def __init__(self, notes_dir: Optional[str] = None):
        super().__init__(
            name="notes",
            description="Create, read, and search personal notes"
        )
        self.notes_dir = Path(notes_dir or Path.home() / ".jarvis" / "notes")
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, query: str, action: str = "search", content: str = "", **kwargs) -> ToolResult:
        """
        Execute notes action.
        
        Args:
            query: Search term or note title
            action: "search", "create", "read", "list"
            content: Note content (for create action)
            
        Returns:
            ToolResult with note data
        """
        try:
            if action == "search":
                results = self._search_notes(query)
            elif action == "create":
                results = self._create_note(query, content)
            elif action == "read":
                results = self._read_note(query)
            elif action == "list":
                results = self._list_notes()
            else:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Unknown action: {action}"
                )

            if results is None:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"No notes found"
                )

            context = f"Notes results:\n\n"
            if isinstance(results, list):
                for note in results:
                    context += f"📝 {note['title']}\n"
                    context += f"   Modified: {note['modified']}\n"
                    context += f"   Preview: {note.get('content', '')[:100]}...\n\n"
            else:
                context += f"Title: {results['title']}\n"
                context += f"Content:\n{results['content']}\n"

            return ToolResult(
                success=True,
                data=results,
                context=context,
                metadata={"action": action, "query": query}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Notes operation failed: {str(e)}"
            )

    def _search_notes(self, query: str) -> Optional[list]:
        """Search notes by title or content."""
        results = []
        query_lower = query.lower()

        for note_file in self.notes_dir.glob("*.json"):
            try:
                with open(note_file, 'r') as f:
                    note = json.load(f)
                    if (query_lower in note['title'].lower() or
                        query_lower in note['content'].lower()):
                        results.append({
                            'title': note['title'],
                            'content': note['content'][:200],
                            'modified': note['modified']
                        })
            except (json.JSONDecodeError, IOError):
                pass

        return results if results else None

    def _create_note(self, title: str, content: str) -> dict:
        """Create a new note."""
        note = {
            'title': title,
            'content': content,
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }

        note_file = self.notes_dir / f"{title.lower().replace(' ', '_')}.json"
        with open(note_file, 'w') as f:
            json.dump(note, f, indent=2)

        return note

    def _read_note(self, title: str) -> Optional[dict]:
        """Read a specific note."""
        note_file = self.notes_dir / f"{title.lower().replace(' ', '_')}.json"

        if note_file.exists():
            with open(note_file, 'r') as f:
                return json.load(f)

        return None

    def _list_notes(self) -> Optional[list]:
        """List all notes."""
        results = []

        for note_file in self.notes_dir.glob("*.json"):
            try:
                with open(note_file, 'r') as f:
                    note = json.load(f)
                    results.append({
                        'title': note['title'],
                        'content': note['content'][:100],
                        'modified': note['modified']
                    })
            except (json.JSONDecodeError, IOError):
                pass

        return results if results else None

    def is_available(self) -> bool:
        """Notes tool is always available."""
        return True
