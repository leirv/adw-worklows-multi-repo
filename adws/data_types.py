"""Data types for ADW system."""

from typing import Optional, List, Literal
from pydantic import BaseModel


# =============================================================================
# Slash Commands
# =============================================================================

# Task type commands
TaskTypeCommand = Literal["/chore", "/bug", "/feature"]

# All slash commands used in the ADW system
SlashCommand = Literal[
    # Task type commands
    "/chore",
    "/bug",
    "/feature",
    # Designer commands
    "/architect",
    "/designer",
    "/ui_designer",
    "/test_tdd_designer",
    # Coder commands
    "/backend_coder",
    "/ui_coder",
    # Validator commands
    "/tester",
]


# =============================================================================
# Agent Execution Models
# =============================================================================

class AgentPromptRequest(BaseModel):
    """Claude Code agent prompt configuration."""
    prompt: str
    agent_id: str
    agent_name: str = "default"
    model: Literal["sonnet", "opus", "haiku"] = "sonnet"
    dangerously_skip_permissions: bool = False
    output_file: Optional[str] = None
    working_directory: Optional[str] = None


class AgentPromptResponse(BaseModel):
    """Claude Code agent response."""
    output: str
    success: bool
    session_id: Optional[str] = None
    cost_usd: Optional[float] = None
    duration_ms: Optional[int] = None


class AgentTemplateRequest(BaseModel):
    """Claude Code agent template execution request."""
    agent_name: str
    slash_command: SlashCommand
    args: List[str]
    agent_id: str
    model: Literal["sonnet", "opus", "haiku"] = "sonnet"
    working_directory: Optional[str] = None


class ClaudeCodeResultMessage(BaseModel):
    """Claude Code JSONL result message (last line)."""
    type: str
    subtype: str
    is_error: bool
    duration_ms: int
    duration_api_ms: int
    num_turns: int
    result: str
    session_id: str
    total_cost_usd: float
