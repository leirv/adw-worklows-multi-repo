# ADW - AI Developer Workflow Library

A Python library for multi-repo agent orchestration using Claude Code CLI.

## Architecture

```
adws/
├── models/                    # Core models
│   ├── __init__.py
│   ├── agent.py               # Agent, AgentConfig, Message
│   └── conversation.py        # Conversation (multi-agent)
├── orchestrator.py            # Multi-repo agent coordination
├── agent.py                   # Claude Code CLI execution
├── git_actions.py             # Generic git operations
├── data_types.py              # Pydantic models
└── utils.py                   # Utilities
```

## Prerequisites

- Claude Code CLI installed and authenticated (`claude --version` works)
- Python 3.10+

## Installation

```bash
# Install dependencies
pip install pydantic

# Or with uv
uv pip install pydantic
```

## Environment Variables

```bash
# Optional - only if claude is not in PATH
export CLAUDE_CODE_PATH="/path/to/claude"
```

**Note:** No API keys needed. This library uses your existing Claude Code CLI authentication.

## Usage

### Basic Execution

```python
from adws.agent import execute_simple, execute_prompt
from adws.data_types import AgentPromptRequest

# Simple execution
response = execute_simple(
    prompt="Explain this codebase",
    model="sonnet",
    working_directory="./my-repo",
)
print(response.output)

# With full configuration
request = AgentPromptRequest(
    prompt="/feature Add user authentication",
    agent_id="abc123",
    agent_name="auth-service",
    model="sonnet",
    working_directory="./repos/auth-service",
    output_file="./agents/abc123/output.jsonl",
)
response = execute_prompt(request)
```

### Multi-Repo Orchestration

```python
from adws.orchestrator import Orchestrator
from adws.models import AgentConfig

# Initialize orchestrator
orchestrator = Orchestrator(project_root="/path/to/project")

# Register agents for repositories
config = AgentConfig(
    name="auth-service",
    repo_path="./repos/auth-service",
    description="Handles user authentication",
    language="python",
    framework="fastapi",
)
agent = orchestrator.register_agent(config)

# Create multi-agent conversation
conversation = orchestrator.create_conversation(["auth-service", "payment-api"])

# Send message to all agents
responses = orchestrator.send_message(
    conversation.id,
    "How should we handle token refresh between services?",
)

# Invite another agent to join
orchestrator.invite_agent(conversation.id, "notification-service")

# Execute command on specific agent
response = orchestrator.execute_command(
    agent_name="auth-service",
    command="/feature",
    args=["Add JWT refresh endpoint"],
)
```

### Git Operations

```python
from adws.git_actions import (
    add_submodule,
    remove_submodule,
    list_submodules,
    create_branch,
    commit,
)

# Submodule management
add_submodule("https://github.com/owner/repo.git", "./repos/repo")
submodules = list_submodules()
remove_submodule("./repos/old-repo")

# Branch operations
create_branch("feat-new-feature")
commit("feat: add new feature")
```

## API Reference

### orchestrator.py

Central coordinator for multi-repo agents.

**Agent Management:**
- `register_agent(config: AgentConfig) -> Agent` - Register a new agent
- `unregister_agent(name: str) -> bool` - Remove an agent
- `get_agent(name: str) -> Optional[Agent]` - Get agent by name
- `list_agents() -> List[str]` - List all agent names

**Conversation Management:**
- `create_conversation(agent_names: List[str]) -> Conversation` - Create conversation
- `get_conversation(id: str) -> Optional[Conversation]` - Get conversation by ID
- `invite_agent(conv_id: str, agent_name: str) -> bool` - Add agent to conversation
- `send_message(conv_id: str, msg: str, targets: List[str]) -> List[AgentResponse]` - Send message

**Direct Execution:**
- `execute_command(agent_name: str, command: str, args: List[str]) -> AgentResponse`

### agent.py

Claude Code CLI execution.

- `execute_simple(prompt: str, model: str, working_directory: str) -> AgentPromptResponse`
- `execute_prompt(request: AgentPromptRequest) -> AgentPromptResponse`
- `execute_template(request: AgentTemplateRequest) -> AgentPromptResponse`

### git_actions.py

Generic git operations.

**Repository:**
- `get_repo_url(cwd: str) -> str`
- `extract_repo_path(url: str) -> str`

**Branch:**
- `get_current_branch(cwd: str) -> str`
- `create_branch(name: str, cwd: str) -> bool`
- `checkout_branch(name: str, cwd: str) -> bool`

**Commit:**
- `stage_all(cwd: str) -> bool`
- `stage_files(files: list, cwd: str) -> bool`
- `commit(message: str, cwd: str) -> bool`

**Submodule:**
- `add_submodule(url: str, path: str, cwd: str) -> bool`
- `remove_submodule(path: str, cwd: str) -> bool`
- `list_submodules(cwd: str) -> list`

### models/

**AgentConfig** - Configuration for an agent
- `name: str` - Agent identifier
- `repo_path: str` - Path to repository
- `description: str` - What the repo does
- `language: str` - Primary language
- `framework: str` - Framework used
- `system_prompt: str` - Custom system prompt

**Agent** - Repository agent
- `config: AgentConfig` - Configuration
- `conversation_history: List[Message]` - Message history
- `add_message(msg: Message)` - Add to history
- `get_context_summary(max: int) -> str` - Get history summary
- `save_config(dir: str)` / `save_history(dir: str)` - Persist to disk
- `Agent.load(dir: str, name: str)` - Load from disk

**Conversation** - Multi-agent conversation
- `id: str` - Unique identifier
- `participants: List[str]` - Agent names
- `messages: List[Message]` - All messages
- `add_participant(name: str, context: str)` - Add agent
- `remove_participant(name: str)` - Remove agent
- `get_context_for_new_participant() -> str` - Summary for joining
- `save(dir: str)` / `Conversation.load(dir: str, id: str)` - Persistence

**Message** - A conversation message
- `role: str` - "user", "assistant", "system"
- `content: str` - Message content
- `agent_id: Optional[str]` - Which agent sent it
- `timestamp: datetime` - When sent

## Output Structure

```
project_root/
├── agents/
│   ├── {agent_name}/
│   │   ├── config.json        # Agent configuration
│   │   └── history.json       # Conversation history
│   └── {execution_id}/
│       └── {agent_name}/
│           └── raw_output.jsonl
├── conversations/
│   └── {conversation_id}.json
└── repos/
    └── {repo_name}/           # Git submodules
```
