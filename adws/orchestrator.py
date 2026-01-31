"""Orchestrator for multi-repo agent coordination."""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from models import Agent, AgentConfig, Message, Conversation
from agent import execute_prompt, execute_template, execute_simple
from data_types import AgentPromptRequest, AgentPromptResponse, AgentTemplateRequest
from utils import make_adw_id


@dataclass
class AgentResponse:
    """Response from an agent execution."""
    agent_name: str
    content: str
    success: bool
    session_id: Optional[str] = None


class Orchestrator:
    """Central coordinator for multi-repo agents."""

    def __init__(self, project_root: str):
        """Initialize the orchestrator.

        Args:
            project_root: Root directory of the project (where repos/, agents/ live)
        """
        self.project_root = project_root
        self.repos_dir = os.path.join(project_root, "repos")
        self.agents_dir = os.path.join(project_root, "agents")
        self.conversations_dir = os.path.join(project_root, "conversations")

        # Ensure directories exist
        os.makedirs(self.repos_dir, exist_ok=True)
        os.makedirs(self.agents_dir, exist_ok=True)
        os.makedirs(self.conversations_dir, exist_ok=True)

        # In-memory registries
        self._agents: Dict[str, Agent] = {}
        self._conversations: Dict[str, Conversation] = {}

        # Load existing agents
        self._load_agents()

    def _load_agents(self) -> None:
        """Load all agents from disk."""
        if not os.path.exists(self.agents_dir):
            return

        for agent_name in os.listdir(self.agents_dir):
            agent_path = os.path.join(self.agents_dir, agent_name)
            if os.path.isdir(agent_path):
                agent = Agent.load(self.agents_dir, agent_name)
                if agent:
                    self._agents[agent_name] = agent

    # =========================================================================
    # Agent Management
    # =========================================================================

    def register_agent(self, config: AgentConfig) -> Agent:
        """Register a new agent.

        Args:
            config: Agent configuration

        Returns:
            The registered Agent instance
        """
        agent = Agent(config)
        agent.save_config(self.agents_dir)
        self._agents[agent.name] = agent
        return agent

    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent.

        Args:
            agent_name: Name of the agent to remove

        Returns:
            True if agent was removed, False if not found
        """
        if agent_name in self._agents:
            del self._agents[agent_name]
            # Note: doesn't delete files, just removes from registry
            return True
        return False

    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get an agent by name."""
        return self._agents.get(agent_name)

    def list_agents(self) -> List[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    def get_all_agents(self) -> Dict[str, Agent]:
        """Get all registered agents."""
        return self._agents.copy()

    # =========================================================================
    # Conversation Management
    # =========================================================================

    def create_conversation(self, agent_names: List[str]) -> Conversation:
        """Create a new conversation with specified agents.

        Args:
            agent_names: List of agent names to include

        Returns:
            The created Conversation instance
        """
        conversation_id = make_adw_id()
        conversation = Conversation(id=conversation_id)

        for agent_name in agent_names:
            agent = self.get_agent(agent_name)
            if agent:
                conversation.add_participant(agent_name)

        conversation.save(self.conversations_dir)
        self._conversations[conversation_id] = conversation
        return conversation

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        # Check in-memory first
        if conversation_id in self._conversations:
            return self._conversations[conversation_id]

        # Try to load from disk
        conversation = Conversation.load(self.conversations_dir, conversation_id)
        if conversation:
            self._conversations[conversation_id] = conversation

        return conversation

    def invite_agent(self, conversation_id: str, agent_name: str) -> bool:
        """Invite an agent to join an existing conversation.

        Args:
            conversation_id: ID of the conversation
            agent_name: Name of the agent to invite

        Returns:
            True if successful, False if conversation or agent not found
        """
        conversation = self.get_conversation(conversation_id)
        agent = self.get_agent(agent_name)

        if not conversation or not agent:
            return False

        # Get context summary for the new participant
        context = conversation.get_context_for_new_participant()
        conversation.add_participant(agent_name, context)
        conversation.save(self.conversations_dir)

        return True

    def remove_agent_from_conversation(self, conversation_id: str, agent_name: str) -> bool:
        """Remove an agent from a conversation."""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False

        conversation.remove_participant(agent_name)
        conversation.save(self.conversations_dir)
        return True

    # =========================================================================
    # Message Routing
    # =========================================================================

    def send_message(
        self,
        conversation_id: str,
        message: str,
        target_agents: Optional[List[str]] = None,
    ) -> List[AgentResponse]:
        """Send a message to agents in a conversation.

        Args:
            conversation_id: ID of the conversation
            message: The message content
            target_agents: Specific agents to target (None = all participants)

        Returns:
            List of responses from each targeted agent
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return []

        # Add user message to conversation
        user_message = Message(role="user", content=message)
        conversation.add_message(user_message)

        # Determine which agents to target
        agents_to_call = target_agents or conversation.participants

        responses = []
        for agent_name in agents_to_call:
            if agent_name not in conversation.participants:
                continue

            agent = self.get_agent(agent_name)
            if not agent:
                continue

            # Execute Claude command for this agent
            response = self._execute_agent(agent, conversation, message)
            responses.append(response)

            # Add agent response to conversation
            if response.success:
                agent_message = Message(
                    role="assistant",
                    content=response.content,
                    agent_id=agent_name,
                )
                conversation.add_message(agent_message)
                agent.add_message(agent_message)

        # Save updated state
        conversation.save(self.conversations_dir)
        for agent_name in agents_to_call:
            agent = self.get_agent(agent_name)
            if agent:
                agent.save_history(self.agents_dir)

        return responses

    def _execute_agent(
        self,
        agent: Agent,
        conversation: Conversation,
        prompt: str,
        model: str = "sonnet",
    ) -> AgentResponse:
        """Execute a Claude command for an agent.

        Args:
            agent: The agent to execute
            conversation: The conversation context
            prompt: The user prompt
            model: Model to use (sonnet, opus, haiku)

        Returns:
            AgentResponse with the result
        """
        # Build context from conversation history
        context_messages = conversation.get_messages_for_agent(agent.name)

        # Build the full prompt with context
        full_prompt = self._build_prompt(agent, context_messages, prompt)

        # Use the agent module to execute
        response = execute_simple(
            prompt=full_prompt,
            model=model,
            working_directory=agent.repo_path,
        )

        return AgentResponse(
            agent_name=agent.name,
            content=response.output,
            success=response.success,
            session_id=response.session_id,
        )

    def _build_prompt(
        self,
        agent: Agent,
        context_messages: List[Message],
        user_prompt: str,
    ) -> str:
        """Build the full prompt for Claude with context.

        Args:
            agent: The agent being invoked
            context_messages: Recent conversation messages
            user_prompt: The current user prompt

        Returns:
            The full prompt string
        """
        parts = []

        # Add agent system prompt if exists
        if agent.config.system_prompt:
            parts.append(f"System: {agent.config.system_prompt}")
            parts.append("")

        # Add agent context
        parts.append(f"You are an agent for the '{agent.name}' repository.")
        parts.append(f"Repository path: {agent.repo_path}")
        if agent.config.description:
            parts.append(f"Repository description: {agent.config.description}")
        parts.append("")

        # Add conversation context
        if context_messages:
            parts.append("Recent conversation context:")
            for msg in context_messages[-10:]:  # Last 10 messages
                prefix = msg.agent_id if msg.agent_id else msg.role
                parts.append(f"[{prefix}]: {msg.content}")
            parts.append("")

        # Add the current prompt
        parts.append(f"User: {user_prompt}")

        return "\n".join(parts)

    # =========================================================================
    # Direct Agent Execution (outside conversation)
    # =========================================================================

    def execute_command(
        self,
        agent_name: str,
        command: str,
        args: List[str] = None,
        model: str = "sonnet",
    ) -> AgentResponse:
        """Execute a slash command on an agent directly.

        Args:
            agent_name: Name of the agent
            command: The slash command (e.g., "/feature", "/bug")
            args: Arguments for the command
            model: Model to use (sonnet, opus, haiku)

        Returns:
            AgentResponse with the result
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return AgentResponse(
                agent_name=agent_name,
                content=f"Agent '{agent_name}' not found",
                success=False,
            )

        # Build prompt from command and args
        prompt = command
        if args:
            prompt += " " + " ".join(args)

        # Use the agent module to execute
        response = execute_simple(
            prompt=prompt,
            model=model,
            working_directory=agent.repo_path,
        )

        return AgentResponse(
            agent_name=agent.name,
            content=response.output,
            success=response.success,
            session_id=response.session_id,
        )

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def get_status(self) -> Dict:
        """Get orchestrator status."""
        return {
            "project_root": self.project_root,
            "agents_count": len(self._agents),
            "agents": list(self._agents.keys()),
            "conversations_count": len(self._conversations),
            "conversations": list(self._conversations.keys()),
        }
