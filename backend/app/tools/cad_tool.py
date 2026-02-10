"""
CAD design helper tool for JARVIS

Help with circuit design and CAD concepts.
Currently supports OpenSCAD suggestions and circuit design help.
"""

from .base import BaseTool, ToolResult
from typing import Optional


class CADTool(BaseTool):
    """Help with circuit design and CAD."""

    def __init__(self):
        super().__init__(
            name="cad_helper",
            description="Help with circuit design, PCB layout, and OpenSCAD modeling"
        )
        self.cad_types = ['circuit', 'pcb', 'openscad', '3d_model']

    def execute(self, query: str, cad_type: str = "circuit", **kwargs) -> ToolResult:
        """
        Execute CAD helper action.
        
        Args:
            query: Design question or concept
            cad_type: "circuit", "pcb", "openscad", "3d_model"
            
        Returns:
            ToolResult with design guidance
        """
        try:
            if cad_type not in self.cad_types:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Unknown CAD type. Use: {', '.join(self.cad_types)}"
                )

            result = self._generate_guidance(query, cad_type)

            context = f"CAD Design Help ({cad_type}):\n\n{result}\n"

            return ToolResult(
                success=True,
                data=result,
                context=context,
                metadata={"cad_type": cad_type, "query": query}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"CAD helper failed: {str(e)}"
            )

    def _generate_guidance(self, query: str, cad_type: str) -> str:
        """Generate CAD design guidance (template for LLM)."""
        guidance_templates = {
            'circuit': f"[LLM should provide circuit design guidance for: {query}]",
            'pcb': f"[LLM should provide PCB layout recommendations for: {query}]",
            'openscad': f"[LLM should provide OpenSCAD modeling help for: {query}]",
            '3d_model': f"[LLM should provide 3D modeling suggestions for: {query}]"
        }
        return guidance_templates.get(cad_type, f"[LLM should help with: {query}]")

    def is_available(self) -> bool:
        """CAD helper is always available."""
        return True
