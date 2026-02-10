"""
Todo tool for JARVIS

Create, update, and manage todo lists.
"""

from .base import BaseTool, ToolResult
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


class TodoTool(BaseTool):
    """Manage todo lists and tasks."""

    def __init__(self, todos_file: Optional[str] = None):
        super().__init__(
            name="todo",
            description="Create and manage todo lists"
        )
        todos_dir = Path(Path.home() / ".jarvis")
        todos_dir.mkdir(parents=True, exist_ok=True)
        self.todos_file = Path(todos_file or todos_dir / "todos.json")
        self._ensure_file()

    def _ensure_file(self):
        """Ensure todos file exists."""
        if not self.todos_file.exists():
            with open(self.todos_file, 'w') as f:
                json.dump({"todos": []}, f, indent=2)

    def execute(self, query: str, action: str = "list", priority: str = "normal", **kwargs) -> ToolResult:
        """
        Execute todo action.
        
        Args:
            query: Todo text or search term
            action: "add", "list", "done", "remove"
            priority: "high", "normal", "low"
            
        Returns:
            ToolResult with todo data
        """
        try:
            if action == "add":
                results = self._add_todo(query, priority)
            elif action == "list":
                results = self._list_todos()
            elif action == "done":
                results = self._mark_done(query)
            elif action == "remove":
                results = self._remove_todo(query)
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
                    error=f"No todos found"
                )

            context = f"Todo list:\n\n"
            if isinstance(results, list):
                for i, todo in enumerate(results, 1):
                    status = "✓" if todo['done'] else "○"
                    priority_icon = "🔴" if todo['priority'] == 'high' else "🟡" if todo['priority'] == 'normal' else "🟢"
                    context += f"{i}. {status} {priority_icon} {todo['text']}\n"
            else:
                context = f"Todo: {results['text']}\nStatus: {'Done' if results['done'] else 'Pending'}\n"

            return ToolResult(
                success=True,
                data=results,
                context=context,
                metadata={"action": action}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Todo operation failed: {str(e)}"
            )

    def _add_todo(self, text: str, priority: str = "normal") -> dict:
        """Add a new todo."""
        with open(self.todos_file, 'r') as f:
            data = json.load(f)

        todo = {
            'id': len(data['todos']) + 1,
            'text': text,
            'priority': priority,
            'done': False,
            'created': datetime.now().isoformat(),
            'due': None
        }

        data['todos'].append(todo)

        with open(self.todos_file, 'w') as f:
            json.dump(data, f, indent=2)

        return todo

    def _list_todos(self) -> Optional[list]:
        """List all todos."""
        with open(self.todos_file, 'r') as f:
            data = json.load(f)

        todos = data.get('todos', [])
        return todos if todos else None

    def _mark_done(self, query: str) -> Optional[dict]:
        """Mark todo as done (by text or id)."""
        with open(self.todos_file, 'r') as f:
            data = json.load(f)

        for todo in data['todos']:
            if str(query).isdigit() and todo['id'] == int(query):
                todo['done'] = True
                with open(self.todos_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return todo
            elif query.lower() in todo['text'].lower():
                todo['done'] = True
                with open(self.todos_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return todo

        return None

    def _remove_todo(self, query: str) -> Optional[list]:
        """Remove a todo."""
        with open(self.todos_file, 'r') as f:
            data = json.load(f)

        for i, todo in enumerate(data['todos']):
            if str(query).isdigit() and todo['id'] == int(query):
                data['todos'].pop(i)
                with open(self.todos_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return data['todos']

        return None

    def is_available(self) -> bool:
        """Todo tool is always available."""
        return True
