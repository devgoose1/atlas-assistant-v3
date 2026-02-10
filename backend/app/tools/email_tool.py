"""
Email tool for JARVIS

Check emails via IMAP protocol.
Supports Gmail, Outlook, and standard IMAP servers.
"""

from .base import BaseTool, ToolResult
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

try:
    import imaplib
    HAS_IMAP = True
except ImportError:
    HAS_IMAP = False


class EmailTool(BaseTool):
    """Check and read emails from IMAP server."""

    def __init__(self, email_config: Optional[Dict[str, Any]] = None):
        super().__init__(
            name="email_checker",
            description="Check your emails and show unread messages"
        )
        # Configuration can be passed or loaded from environment
        self.config = email_config or {
            "imap_server": None,
            "email": None,
            "password": None
        }

    def execute(self, query: str = "unread", mailbox: str = "INBOX", max_results: int = 5, **kwargs) -> ToolResult:
        """
        Execute email check.
        
        Args:
            query: "unread", "today", "week", or sender name
            mailbox: Email folder (default INBOX)
            max_results: Maximum emails to return
            
        Returns:
            ToolResult with email list
        """
        if not self.is_available():
            return ToolResult(
                success=False,
                data=None,
                error="Email tool not available (IMAP not configured or imaplib unavailable)"
            )

        try:
            emails = self._fetch_emails(mailbox, query, max_results)

            if not emails:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"No emails found in {mailbox}"
                )

            # Format context for LLM
            context = f"Emails in {mailbox}:\n\n"
            for i, email in enumerate(emails, 1):
                context += f"{i}. From: {email['from']}\n"
                context += f"   Subject: {email['subject']}\n"
                context += f"   Date: {email['date']}\n"
                if email.get('preview'):
                    context += f"   Preview: {email['preview'][:100]}...\n"
                context += "\n"

            return ToolResult(
                success=True,
                data=emails,
                context=context,
                metadata={"mailbox": mailbox, "query": query, "count": len(emails)}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Email check failed: {str(e)}"
            )

    def _fetch_emails(self, mailbox: str, query: str, max_results: int) -> list:
        """Fetch emails from IMAP server."""
        # Note: This is a placeholder. In production, you'd implement actual IMAP connection
        # For now, return a mock response to show the structure
        return [
            {
                "from": "friend@example.com",
                "subject": "Coffee tomorrow?",
                "date": datetime.now().isoformat(),
                "preview": "Hey, want to grab coffee tomorrow at 3pm?"
            }
        ]

    def is_available(self) -> bool:
        """Check if email tool is available."""
        # Check if IMAP is available and credentials are configured
        if not HAS_IMAP:
            return False

        # In production, check if email credentials are set
        has_config = all([
            self.config.get("imap_server"),
            self.config.get("email"),
            self.config.get("password")
        ])
        return False  # Disabled by default, enable when credentials are provided
