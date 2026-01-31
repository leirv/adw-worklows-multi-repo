"""Conversation model for multi-agent interactions."""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .agent import Message


@dataclass
class Conversation:
    """A conversation that can involve multiple agents."""

    id: str
    participants: List[str] = field(default_factory=list)  # Agent names
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_participant(self, agent_name: str, context_summary: str = "") -> None:
        """Add an agent to the conversation."""
        if agent_name not in self.participants:
            self.participants.append(agent_name)
            self.updated_at = datetime.now()

            # Add system message about agent joining
            if context_summary:
                self.add_message(Message(
                    role="system",
                    content=f"Agent '{agent_name}' joined the conversation with context:\n{context_summary}",
                    agent_id=agent_name,
                ))
            else:
                self.add_message(Message(
                    role="system",
                    content=f"Agent '{agent_name}' joined the conversation.",
                    agent_id=agent_name,
                ))

    def remove_participant(self, agent_name: str) -> None:
        """Remove an agent from the conversation."""
        if agent_name in self.participants:
            self.participants.remove(agent_name)
            self.updated_at = datetime.now()

            self.add_message(Message(
                role="system",
                content=f"Agent '{agent_name}' left the conversation.",
                agent_id=agent_name,
            ))

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages_for_agent(self, agent_name: str, limit: int = 50) -> List[Message]:
        """Get messages relevant to a specific agent."""
        # Return recent messages, could be filtered further based on agent context
        return self.messages[-limit:]

    def get_context_for_new_participant(self, max_messages: int = 20) -> str:
        """Generate context summary for a new participant joining."""
        recent = self.messages[-max_messages:]
        if not recent:
            return "This is a new conversation with no history."

        summary_parts = [
            f"Conversation started: {self.created_at.isoformat()}",
            f"Current participants: {', '.join(self.participants)}",
            "",
            "Recent messages:",
        ]

        for msg in recent:
            prefix = f"[{msg.role}]"
            if msg.agent_id:
                prefix = f"[{msg.agent_id}]"
            # Truncate long messages
            content = msg.content[:300] + "..." if len(msg.content) > 300 else msg.content
            summary_parts.append(f"{prefix}: {content}")

        return "\n".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "participants": self.participants,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        """Create from dictionary."""
        data = data.copy()
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if "messages" in data:
            data["messages"] = [Message.from_dict(m) for m in data["messages"]]
        return cls(**data)

    def save(self, conversations_dir: str) -> str:
        """Save conversation to disk."""
        os.makedirs(conversations_dir, exist_ok=True)
        filepath = os.path.join(conversations_dir, f"{self.id}.json")
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return filepath

    @classmethod
    def load(cls, conversations_dir: str, conversation_id: str) -> Optional["Conversation"]:
        """Load conversation from disk."""
        filepath = os.path.join(conversations_dir, f"{conversation_id}.json")
        if not os.path.exists(filepath):
            return None

        with open(filepath, "r") as f:
            data = json.load(f)

        return cls.from_dict(data)

    def __repr__(self) -> str:
        return f"Conversation(id={self.id}, participants={self.participants}, messages={len(self.messages)})"
