"""Agent model for multi-repo orchestration."""

import os
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    repo_path: str
    description: str = ""
    language: str = ""
    framework: str = ""
    entry_points: List[str] = field(default_factory=list)
    system_prompt: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "repo_path": self.repo_path,
            "description": self.description,
            "language": self.language,
            "framework": self.framework,
            "entry_points": self.entry_points,
            "system_prompt": self.system_prompt,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        """Create from dictionary."""
        data = data.copy()
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class Message:
    """A message in a conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    agent_id: Optional[str] = None  # Which agent sent/received this
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "role": self.role,
            "content": self.content,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create from dictionary."""
        data = data.copy()
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class Agent:
    """An agent that manages a single repository."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.conversation_history: List[Message] = []
        self._session_id: Optional[str] = None

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def repo_path(self) -> str:
        return self.config.repo_path

    def add_message(self, message: Message) -> None:
        """Add a message to conversation history."""
        self.conversation_history.append(message)

    def get_context_summary(self, max_messages: int = 10) -> str:
        """Get a summary of recent conversation for context sharing."""
        recent = self.conversation_history[-max_messages:]
        if not recent:
            return "No conversation history."

        summary_parts = []
        for msg in recent:
            prefix = f"[{msg.role}]"
            if msg.agent_id:
                prefix = f"[{msg.role} - {msg.agent_id}]"
            summary_parts.append(f"{prefix}: {msg.content[:200]}...")

        return "\n".join(summary_parts)

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        self._session_id = None

    def save_config(self, agents_dir: str) -> str:
        """Save agent config to disk."""
        agent_dir = os.path.join(agents_dir, self.name)
        os.makedirs(agent_dir, exist_ok=True)

        config_path = os.path.join(agent_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(self.config.to_dict(), f, indent=2)

        return config_path

    def save_history(self, agents_dir: str) -> str:
        """Save conversation history to disk."""
        agent_dir = os.path.join(agents_dir, self.name)
        os.makedirs(agent_dir, exist_ok=True)

        history_path = os.path.join(agent_dir, "history.json")
        history_data = [msg.to_dict() for msg in self.conversation_history]
        with open(history_path, "w") as f:
            json.dump(history_data, f, indent=2)

        return history_path

    @classmethod
    def load(cls, agents_dir: str, agent_name: str) -> Optional["Agent"]:
        """Load an agent from disk."""
        config_path = os.path.join(agents_dir, agent_name, "config.json")

        if not os.path.exists(config_path):
            return None

        with open(config_path, "r") as f:
            config_data = json.load(f)

        config = AgentConfig.from_dict(config_data)
        agent = cls(config)

        # Load history if exists
        history_path = os.path.join(agents_dir, agent_name, "history.json")
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history_data = json.load(f)
            agent.conversation_history = [Message.from_dict(m) for m in history_data]

        return agent

    def __repr__(self) -> str:
        return f"Agent(name={self.name}, repo={self.repo_path})"
