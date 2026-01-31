# Project Builder

Generate the complete ADW (AI Developer Workflow) multi-repo project structure. This command creates all directories, command templates, and Python library files.

## Instructions

- Create ALL directories and files listed below
- Do not skip any file - the system requires all components
- Use the exact content provided for each file
- After creating all files, report what was created

## Directory Structure

Create the following directories:
```
./
├── .claude/commands/
│   ├── tasks/
│   └── git-actions/
├── adws/
│   └── models/
├── repos/
├── agents/
├── conversations/
├── specs/
├── adr/
├── ddr/
├── udr/
├── tdr/
└── app/
    ├── server/
    └── client/
```

## Command Templates

### .claude/commands/tasks/classifier.md
```markdown
# Task Classifier

Analyze the `Task` and classify it into the appropriate command type. Return ONLY the command - nothing else.

## Instructions

- IMPORTANT: You must return ONLY the command string. No explanations, no reasoning, no extra text.
- Analyze the task description to determine the type of work required.
- Match the task to ONE of the available commands based on the classification rules below.
- If the task is unclear or doesn't fit any category, return `0`.

## Classification Rules

### Planning Commands (create specs/records BEFORE implementation)

| Command | Use When |
|---------|----------|
| `/architect` | System-level decisions, technology choices, component structure, API design |
| `/designer` | Code-level design, class structure, method flows, service interactions |
| `/ui_designer` | UI/UX design, screens, components, user flows, layouts |
| `/test_tdd_designer` | Test design, TDD approach, defining tests before implementation |
| `/feature` | New functionality, adding capabilities, enhancements |
| `/bug` | Fixing errors, crashes, incorrect behavior, regressions |
| `/chore` | Maintenance, refactoring, dependencies, documentation, cleanup |

### Implementation Commands (execute plans)

| Command | Use When |
|---------|----------|
| `/backend_coder` | Implementing server-side code, APIs, services, Python code |
| `/ui_coder` | Implementing frontend code, components, UI, React/Vue/Vite |
| `/tester` | Running tests, validating implementation, final QA |

## Task

$ARGUMENTS

## Response Format

Return ONLY one of: `/architect`, `/designer`, `/ui_designer`, `/test_tdd_designer`, `/feature`, `/bug`, `/chore`, `/backend_coder`, `/ui_coder`, `/tester`, or `0`
```

### .claude/commands/tasks/architect.md
```markdown
# Architect

Create a new ADR (Architectural Decision Record) in `adr/*.md` using the `Plan Format`. Follow the `Instructions` and `Report` results.

## Instructions

- You're writing an ADR that provides foundational architectural rules for the application.
- Create the ADR in the `adr/*.md` file. Name it appropriately based on the Task.
- Research the codebase and put together a plan to accomplish the Task.
- Replace every <placeholder> in the Plan Format with the requested value.
- Start your research by reading the `README.md` file.

## Plan Format

\`\`\`md
# Task: <Task name>

## Task Description
<describe the Task in detail>

## Relevant Files
<list files relevant to the task>

## Step by Step Tasks
<list step by step tasks as h3 headers plus bullet points>

## Validation Commands
- `cd app/server && uv run pytest`

## Notes
<additional notes>
\`\`\`

## Task
$ARGUMENTS

## Report
- Summarize work done in bullet points
- Include path to the ADR created
```

### .claude/commands/tasks/designer.md
```markdown
# Designer

Create a new DDR (Design Decision Record) in `ddr/*.md` for code-level design.

## Instructions

- Write a DDR that provides code-level design (classes, methods, data flow).
- Create the DDR in `ddr/*.md`. Name it based on the Task.
- Research existing patterns before designing new ones.

## Plan Format

\`\`\`md
# Task: <Task name>

## Task Description
<describe the Task>

## Design Overview
<high-level design approach>

## Class/Service Design

### <ClassName>
- **Responsibility**: <single responsibility>
- **Location**: <file path>
- **Dependencies**: <list dependencies>

#### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|

## Data Flow
<describe data flow with arrow notation>

## Method Contracts
### <ClassName.methodName>
- **Input**: <expected input>
- **Output**: <expected output>
- **Errors**: <error conditions>

## Step by Step Tasks
<implementation steps>

## Validation Commands
- `cd app/server && uv run pytest`
\`\`\`

## Task
$ARGUMENTS

## Report
- Summarize work in bullet points
- Include path to DDR created
```

### .claude/commands/tasks/ui_designer.md
```markdown
# UI Designer

Create a new UDR (UI Decision Record) in `udr/*.md` for UI/UX design.

## Instructions

- Write a UDR for user interface, screens, components, and user flows.
- Create the UDR in `udr/*.md`. Name it based on the Task.
- Research existing UI patterns before designing.

## Plan Format

\`\`\`md
# Task: <Task name>

## Task Description
<describe the Task>

## UI Overview
<high-level UI approach>

## User Flow
\`\`\`mermaid
flowchart LR
    A[Screen A] --> B[Action]
    B --> C[Screen B]
\`\`\`

## Screens/Views

### <Screen Name>
- **Route**: <URL path>
- **Purpose**: <what user accomplishes>

#### Components Used
| Component | Purpose | Props/Data |
|-----------|---------|------------|

#### User Interactions
| Element | Action | Result |
|---------|--------|--------|

## Component Design

### <ComponentName>
- **Location**: <file path>
- **Props**: <prop definitions>
- **State**: <state definitions>

## API Integration
| Screen | Endpoint | Method | Purpose |
|--------|----------|--------|---------|

## Validation Commands
- `cd app/client && npm run test`
- `cd app/client && npm run build`
\`\`\`

## Task
$ARGUMENTS

## Report
- Summarize work in bullet points
- Include path to UDR created
```

### .claude/commands/tasks/test_tdd_designer.md
```markdown
# TDD Test Designer

Create a new TDR (Test Design Record) in `tdr/*.md` to define tests BEFORE implementation.

## Instructions

- Write a TDR that defines tests to DRIVE implementation (TDD).
- Create tests from perspective: "What should this code DO?"
- Create the TDR in `tdr/*.md`. Name it based on the Task.

## Plan Format

\`\`\`md
# Task: <Task name>

## Task Description
<what needs to be built/tested>

## Test Strategy Overview
<testing approach>

## Backend Tests

### <TestClassName>
- **File**: `app/server/tests/test_<name>.py`

#### Test Cases
| Test Name | Description | Input | Expected Output |
|-----------|-------------|-------|-----------------|

## Frontend Tests

### <ComponentName>.test.tsx
- **File**: `app/client/src/__tests__/<name>.test.tsx`

#### Test Cases
| Test Name | Description | Setup | Expected Behavior |
|-----------|-------------|-------|-------------------|

## Mocks and Fixtures
| Mock | Purpose | Returns |
|------|---------|---------|

## Definition of Done
- [ ] All test cases implemented
- [ ] All tests pass
- [ ] Edge cases covered
\`\`\`

## Task
$ARGUMENTS

## Report
- Summarize work in bullet points
- Include path to TDR created
- List total test cases defined
```

### .claude/commands/tasks/feature.md
```markdown
# Feature Planning

Create a new plan in `specs/*.md` to implement the Feature.

## Instructions

- Write a plan to implement a new feature that adds value.
- Create the plan in `specs/*.md`. Name it based on the Feature.
- Research existing patterns before planning.
- Follow existing conventions in the codebase.

## Plan Format

\`\`\`md
# Feature: <feature name>

## Feature Description
<describe feature and value to users>

## User Story
As a <user type>
I want to <action>
So that <benefit>

## Problem Statement
<problem this feature addresses>

## Solution Statement
<proposed solution approach>

## Relevant Files
<files to modify/create>

## Implementation Plan
### Phase 1: Foundation
### Phase 2: Core Implementation
### Phase 3: Integration

## Step by Step Tasks
<detailed implementation steps>

## Testing Strategy
### Unit Tests
### Integration Tests
### Edge Cases

## Acceptance Criteria
<measurable criteria for completion>

## Validation Commands
- `cd app/server && uv run pytest`
\`\`\`

## Feature
$ARGUMENTS

## Report
- Summarize work in bullet points
- Include path to spec created
```

### .claude/commands/tasks/bug.md
```markdown
# Bug Planning

Create a new plan in `specs/*.md` to resolve the Bug.

## Instructions

- Write a plan to resolve a bug - thorough and precise.
- Create the plan in `specs/*.md`. Name it based on the Bug.
- Research to understand the bug and find root cause.
- Be surgical - minimal changes to fix the bug.

## Plan Format

\`\`\`md
# Bug: <bug name>

## Bug Description
<describe bug, symptoms, expected vs actual>

## Problem Statement
<specific problem to solve>

## Solution Statement
<proposed fix approach>

## Steps to Reproduce
<exact steps to reproduce>

## Root Cause Analysis
<explain root cause>

## Relevant Files
<files to fix>

## Step by Step Tasks
<fix steps with validation>

## Validation Commands
- `cd app/server && uv run pytest`
\`\`\`

## Bug
$ARGUMENTS

## Report
- Summarize work in bullet points
- Include path to spec created
```

### .claude/commands/tasks/chore.md
```markdown
# Chore Planning

Create a new plan in `specs/*.md` to resolve the Chore.

## Instructions

- Write a plan for maintenance/chore task.
- Create the plan in `specs/*.md`. Name it based on the Chore.
- Be thorough so we don't waste time with second rounds.

## Plan Format

\`\`\`md
# Chore: <chore name>

## Chore Description
<describe the chore>

## Relevant Files
<files to modify>

## Step by Step Tasks
<chore steps>

## Validation Commands
- `cd app/server && uv run pytest`
\`\`\`

## Chore
$ARGUMENTS

## Report
- Summarize work in bullet points
- Include path to spec created
```

### .claude/commands/tasks/backend_coder.md
```markdown
# Backend Coder

Implement backend code following the Plan.

## Instructions

- Read the plan thoroughly before writing code.
- Focus ONLY on backend/server code (Python, APIs, services).
- Follow existing patterns in `app/server/**`.
- If DDR exists, follow its class/method contracts.
- If TDR exists, ensure implementation passes defined tests.
- Run tests after implementation.

## Relevant Files
- `app/server/**` - Backend codebase
- `ddr/*.md` - Design Decision Records
- `tdr/*.md` - Test Design Records

## Validation Commands
- `cd app/server && uv run pytest`

## Plan
$ARGUMENTS

## Report
- Summarize work in bullet points
- List files created/modified
- Report `git diff --stat`
- Confirm tests pass
```

### .claude/commands/tasks/ui_coder.md
```markdown
# UI Coder

Implement frontend code following the Plan.

## Instructions

- Read the plan thoroughly before writing code.
- Focus ONLY on frontend/client code (Vite, React/Vue).
- Follow existing patterns in `app/client/**`.
- If UDR exists, follow its component design.
- If TDR exists, ensure implementation passes defined tests.
- Ensure accessibility (ARIA, keyboard nav).

## Relevant Files
- `app/client/**` - Frontend codebase
- `udr/*.md` - UI Decision Records
- `tdr/*.md` - Test Design Records

## Validation Commands
- `cd app/client && npm run test`
- `cd app/client && npm run build`

## Plan
$ARGUMENTS

## Report
- Summarize work in bullet points
- List files/components created/modified
- Report `git diff --stat`
- Confirm tests pass and build succeeds
```

### .claude/commands/tasks/tester.md
```markdown
# Tester

Perform final validation of implementation against the Plan.

## Instructions

- You are the final quality gate before code is complete.
- Read the plan and all design records (ADR, DDR, UDR, TDR).
- Verify implementation matches specifications.
- Run ALL tests and ensure they pass.
- Check for regressions.

## Validation Checklist

### Code Quality
- [ ] Follows coding standards
- [ ] No obvious bugs
- [ ] Proper error handling

### Test Coverage
- [ ] All TDR test cases implemented
- [ ] Unit tests pass
- [ ] Integration tests pass

### Backend (if applicable)
- [ ] `cd app/server && uv run pytest` passes

### Frontend (if applicable)
- [ ] `cd app/client && npm run test` passes
- [ ] `cd app/client && npm run build` succeeds

## Plan
$ARGUMENTS

## Report Format
\`\`\`
## Validation Results

### Tests
- Backend: X passed, Y failed
- Frontend: X passed, Y failed

### Issues Found
- <issues or "None">

### Final Verdict: PASS / FAIL
\`\`\`
```

## Python Library (adws/)

### adws/\_\_init\_\_.py
```python
"""ADW - AI Developer Workflow Library."""
```

### adws/models/\_\_init\_\_.py
```python
"""Models for ADW multi-repo orchestration."""

from .agent import Agent, AgentConfig, Message
from .conversation import Conversation

__all__ = ["Agent", "AgentConfig", "Message", "Conversation"]
```

### adws/models/agent.py
```python
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
        data = data.copy()
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class Message:
    """A message in a conversation."""
    role: str
    content: str
    agent_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
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
        self.conversation_history.append(message)

    def get_context_summary(self, max_messages: int = 10) -> str:
        recent = self.conversation_history[-max_messages:]
        if not recent:
            return "No conversation history."
        parts = []
        for msg in recent:
            prefix = f"[{msg.role}]" if not msg.agent_id else f"[{msg.agent_id}]"
            parts.append(f"{prefix}: {msg.content[:200]}...")
        return "\n".join(parts)

    def clear_history(self) -> None:
        self.conversation_history = []
        self._session_id = None

    def save_config(self, agents_dir: str) -> str:
        agent_dir = os.path.join(agents_dir, self.name)
        os.makedirs(agent_dir, exist_ok=True)
        config_path = os.path.join(agent_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(self.config.to_dict(), f, indent=2)
        return config_path

    def save_history(self, agents_dir: str) -> str:
        agent_dir = os.path.join(agents_dir, self.name)
        os.makedirs(agent_dir, exist_ok=True)
        history_path = os.path.join(agent_dir, "history.json")
        with open(history_path, "w") as f:
            json.dump([m.to_dict() for m in self.conversation_history], f, indent=2)
        return history_path

    @classmethod
    def load(cls, agents_dir: str, agent_name: str) -> Optional["Agent"]:
        config_path = os.path.join(agents_dir, agent_name, "config.json")
        if not os.path.exists(config_path):
            return None
        with open(config_path, "r") as f:
            config = AgentConfig.from_dict(json.load(f))
        agent = cls(config)
        history_path = os.path.join(agents_dir, agent_name, "history.json")
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                agent.conversation_history = [Message.from_dict(m) for m in json.load(f)]
        return agent
```

### adws/models/conversation.py
```python
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
    participants: List[str] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_participant(self, agent_name: str, context_summary: str = "") -> None:
        if agent_name not in self.participants:
            self.participants.append(agent_name)
            self.updated_at = datetime.now()
            msg = f"Agent '{agent_name}' joined."
            if context_summary:
                msg = f"Agent '{agent_name}' joined with context:\n{context_summary}"
            self.add_message(Message(role="system", content=msg, agent_id=agent_name))

    def remove_participant(self, agent_name: str) -> None:
        if agent_name in self.participants:
            self.participants.remove(agent_name)
            self.updated_at = datetime.now()
            self.add_message(Message(role="system", content=f"Agent '{agent_name}' left.", agent_id=agent_name))

    def add_message(self, message: Message) -> None:
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages_for_agent(self, agent_name: str, limit: int = 50) -> List[Message]:
        return self.messages[-limit:]

    def get_context_for_new_participant(self, max_messages: int = 20) -> str:
        recent = self.messages[-max_messages:]
        if not recent:
            return "New conversation with no history."
        parts = [f"Participants: {', '.join(self.participants)}", "", "Recent:"]
        for msg in recent:
            prefix = msg.agent_id or msg.role
            content = msg.content[:300] + "..." if len(msg.content) > 300 else msg.content
            parts.append(f"[{prefix}]: {content}")
        return "\n".join(parts)

    def to_dict(self) -> Dict[str, Any]:
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
        data = data.copy()
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if "messages" in data:
            data["messages"] = [Message.from_dict(m) for m in data["messages"]]
        return cls(**data)

    def save(self, conversations_dir: str) -> str:
        os.makedirs(conversations_dir, exist_ok=True)
        filepath = os.path.join(conversations_dir, f"{self.id}.json")
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return filepath

    @classmethod
    def load(cls, conversations_dir: str, conversation_id: str) -> Optional["Conversation"]:
        filepath = os.path.join(conversations_dir, f"{conversation_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            return cls.from_dict(json.load(f))
```

### adws/data_types.py
```python
"""Data types for ADW system."""

from typing import Optional, List, Literal
from pydantic import BaseModel

TaskTypeCommand = Literal["/chore", "/bug", "/feature"]

SlashCommand = Literal[
    "/classifier",
    "/chore", "/bug", "/feature",
    "/architect", "/designer", "/ui_designer", "/test_tdd_designer",
    "/backend_coder", "/ui_coder",
    "/tester",
]


class AgentPromptRequest(BaseModel):
    prompt: str
    agent_id: str
    agent_name: str = "default"
    model: Literal["sonnet", "opus", "haiku"] = "sonnet"
    dangerously_skip_permissions: bool = False
    output_file: Optional[str] = None
    working_directory: Optional[str] = None


class AgentPromptResponse(BaseModel):
    output: str
    success: bool
    session_id: Optional[str] = None
    cost_usd: Optional[float] = None
    duration_ms: Optional[int] = None


class AgentTemplateRequest(BaseModel):
    agent_name: str
    slash_command: SlashCommand
    args: List[str]
    agent_id: str
    model: Literal["sonnet", "opus", "haiku"] = "sonnet"
    working_directory: Optional[str] = None
```

### adws/utils.py
```python
"""Utility functions for ADW system."""

import uuid

def make_adw_id() -> str:
    """Generate a short 8-character UUID."""
    return str(uuid.uuid4())[:8]
```

### adws/agent.py
```python
"""Claude Code agent module for executing prompts."""

import subprocess
import os
import json
from typing import Optional, List, Dict, Any, Tuple
from data_types import AgentPromptRequest, AgentPromptResponse, AgentTemplateRequest

CLAUDE_PATH = os.getenv("CLAUDE_CODE_PATH", "claude")


def check_claude_installed() -> Optional[str]:
    try:
        result = subprocess.run([CLAUDE_PATH, "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return f"Claude Code CLI not installed at: {CLAUDE_PATH}"
    except FileNotFoundError:
        return f"Claude Code CLI not found at: {CLAUDE_PATH}"
    return None


def execute_prompt(request: AgentPromptRequest) -> AgentPromptResponse:
    error = check_claude_installed()
    if error:
        return AgentPromptResponse(output=error, success=False)

    cmd = [CLAUDE_PATH, "-p", request.prompt, "--model", request.model]
    if request.dangerously_skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    cwd = request.working_directory or os.getcwd()

    try:
        if request.output_file:
            cmd.extend(["--output-format", "stream-json", "--verbose"])
            os.makedirs(os.path.dirname(request.output_file), exist_ok=True)
            with open(request.output_file, "w") as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, cwd=cwd)
            if result.returncode == 0:
                with open(request.output_file) as f:
                    for line in reversed(f.readlines()):
                        if line.strip():
                            msg = json.loads(line)
                            if msg.get("type") == "result":
                                return AgentPromptResponse(
                                    output=msg.get("result", ""),
                                    success=not msg.get("is_error", False),
                                    session_id=msg.get("session_id"),
                                )
            return AgentPromptResponse(output=f"Error: {result.stderr}", success=False)
        else:
            cmd.extend(["--output-format", "text"])
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
            return AgentPromptResponse(
                output=result.stdout.strip() if result.returncode == 0 else result.stderr,
                success=result.returncode == 0,
            )
    except Exception as e:
        return AgentPromptResponse(output=f"Error: {e}", success=False)


def execute_simple(prompt: str, model: str = "sonnet", working_directory: Optional[str] = None) -> AgentPromptResponse:
    from utils import make_adw_id
    return execute_prompt(AgentPromptRequest(
        prompt=prompt,
        agent_id=make_adw_id(),
        agent_name="simple",
        model=model,
        working_directory=working_directory,
    ))
```

### adws/git_actions.py
```python
"""Git operations module."""

import subprocess
from typing import Optional, Tuple, List


def run_git_command(args: list, cwd: Optional[str] = None) -> Tuple[bool, str, str]:
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def get_repo_url(cwd: Optional[str] = None) -> str:
    success, stdout, stderr = run_git_command(["remote", "get-url", "origin"], cwd)
    if not success:
        raise ValueError(f"Failed to get remote URL: {stderr}")
    return stdout


def extract_repo_path(url: str) -> str:
    if url.startswith("git@"):
        url = url.split(":")[-1]
    for prefix in ["https://github.com/", "https://gitlab.com/", "https://bitbucket.org/"]:
        url = url.replace(prefix, "")
    return url.rstrip(".git")


def create_branch(name: str, cwd: Optional[str] = None) -> bool:
    success, _, _ = run_git_command(["checkout", "-b", name], cwd)
    return success


def checkout_branch(name: str, cwd: Optional[str] = None) -> bool:
    success, _, _ = run_git_command(["checkout", name], cwd)
    return success


def commit(message: str, cwd: Optional[str] = None) -> bool:
    success, _, _ = run_git_command(["commit", "-m", message], cwd)
    return success


def stage_all(cwd: Optional[str] = None) -> bool:
    success, _, _ = run_git_command(["add", "-A"], cwd)
    return success


def add_submodule(url: str, path: str, cwd: Optional[str] = None) -> bool:
    success, _, _ = run_git_command(["submodule", "add", url, path], cwd)
    return success


def remove_submodule(path: str, cwd: Optional[str] = None) -> bool:
    run_git_command(["submodule", "deinit", "-f", path], cwd)
    success, _, _ = run_git_command(["rm", "-f", path], cwd)
    return success


def list_submodules(cwd: Optional[str] = None) -> List[str]:
    success, stdout, _ = run_git_command(["submodule", "status"], cwd)
    if not success or not stdout:
        return []
    return [line.split()[1] for line in stdout.split("\n") if line.strip()]
```

### adws/orchestrator.py
```python
"""Orchestrator for multi-repo agent coordination."""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass

from models import Agent, AgentConfig, Message, Conversation
from agent import execute_simple
from utils import make_adw_id


@dataclass
class AgentResponse:
    agent_name: str
    content: str
    success: bool
    session_id: Optional[str] = None


class Orchestrator:
    VALID_COMMANDS = [
        "/architect", "/designer", "/ui_designer", "/test_tdd_designer",
        "/feature", "/bug", "/chore",
        "/backend_coder", "/ui_coder", "/tester",
    ]

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.repos_dir = os.path.join(project_root, "repos")
        self.agents_dir = os.path.join(project_root, "agents")
        self.conversations_dir = os.path.join(project_root, "conversations")
        for d in [self.repos_dir, self.agents_dir, self.conversations_dir]:
            os.makedirs(d, exist_ok=True)
        self._agents: Dict[str, Agent] = {}
        self._conversations: Dict[str, Conversation] = {}
        self._load_agents()

    def _load_agents(self):
        if not os.path.exists(self.agents_dir):
            return
        for name in os.listdir(self.agents_dir):
            if os.path.isdir(os.path.join(self.agents_dir, name)):
                agent = Agent.load(self.agents_dir, name)
                if agent:
                    self._agents[name] = agent

    def register_agent(self, config: AgentConfig) -> Agent:
        agent = Agent(config)
        agent.save_config(self.agents_dir)
        self._agents[agent.name] = agent
        return agent

    def get_agent(self, name: str) -> Optional[Agent]:
        return self._agents.get(name)

    def list_agents(self) -> List[str]:
        return list(self._agents.keys())

    def create_conversation(self, agent_names: List[str]) -> Conversation:
        conv = Conversation(id=make_adw_id())
        for name in agent_names:
            if self.get_agent(name):
                conv.add_participant(name)
        conv.save(self.conversations_dir)
        self._conversations[conv.id] = conv
        return conv

    def classify_task(self, agent_name: str, task: str, model: str = "haiku") -> Optional[str]:
        agent = self.get_agent(agent_name)
        if not agent:
            return None
        response = execute_simple(f"/classifier {task}", model, agent.repo_path)
        if not response.success:
            return None
        result = response.output.strip()
        return result if result in self.VALID_COMMANDS else None

    def classify_and_execute(self, agent_name: str, task: str, classifier_model: str = "haiku", execution_model: str = "sonnet") -> AgentResponse:
        agent = self.get_agent(agent_name)
        if not agent:
            return AgentResponse(agent_name, f"Agent '{agent_name}' not found", False)
        command = self.classify_task(agent_name, task, classifier_model)
        if not command:
            return AgentResponse(agent_name, "Failed to classify task", False)
        return self.execute_command(agent_name, command, [task], execution_model)

    def execute_command(self, agent_name: str, command: str, args: List[str] = None, model: str = "sonnet") -> AgentResponse:
        agent = self.get_agent(agent_name)
        if not agent:
            return AgentResponse(agent_name, f"Agent '{agent_name}' not found", False)
        prompt = command + (" " + " ".join(args) if args else "")
        response = execute_simple(prompt, model, agent.repo_path)
        return AgentResponse(agent_name, response.output, response.success, response.session_id)

    def get_status(self) -> Dict:
        return {
            "project_root": self.project_root,
            "agents": list(self._agents.keys()),
            "conversations": list(self._conversations.keys()),
        }
```

## Task

$ARGUMENTS

## Report

After creating all files, report:
- Total directories created
- Total files created
- Any errors encountered
