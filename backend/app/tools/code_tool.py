"""
Code analysis tool for JARVIS

Analyze code, answer coding questions, and help with debugging.
"""

from .base import BaseTool, ToolResult
from pathlib import Path
from typing import Optional


class CodeTool(BaseTool):
    """Help with code analysis and programming."""

    def __init__(self):
        super().__init__(
            name="code_helper",
            description="Analyze code, answer programming questions, debug"
        )
        self.supported_languages = {
            'python', 'javascript', 'typescript', 'java', 'c', 'cpp',
            'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin'
        }

    def execute(self, query: str, action: str = "explain", code: str = "", language: str = "", **kwargs) -> ToolResult:
        """
        Execute code helper action.
        
        Args:
            query: Coding question or topic
            action: "explain", "debug", "optimize", "refactor"
            code: Code snippet to analyze
            language: Programming language
            
        Returns:
            ToolResult with code analysis
        """
        try:
            if action == "explain":
                result = self._explain_concept(query)
            elif action == "debug":
                result = self._debug_code(code, language)
            elif action == "optimize":
                result = self._optimize_code(code, language)
            elif action == "refactor":
                result = self._refactor_code(code, language)
            else:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Unknown action: {action}"
                )

            context = f"Code Analysis Result:\n\n{result}\n"

            return ToolResult(
                success=True,
                data=result,
                context=context,
                metadata={"action": action, "language": language}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Code analysis failed: {str(e)}"
            )

    def _explain_concept(self, topic: str) -> str:
        """Explain a coding concept (template for LLM to fill in)."""
        return f"[LLM should explain: {topic}]"

    def _debug_code(self, code: str, language: str) -> str:
        """Suggest debugging approach for code."""
        return f"[LLM should debug {language} code]"

    def _optimize_code(self, code: str, language: str) -> str:
        """Suggest code optimizations."""
        return f"[LLM should optimize {language} code]"

    def _refactor_code(self, code: str, language: str) -> str:
        """Suggest code refactoring."""
        return f"[LLM should refactor {language} code]"

    def is_available(self) -> bool:
        """Code helper is always available."""
        return True
