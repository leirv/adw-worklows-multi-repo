"""Claude Code agent module for executing prompts programmatically.

This module assumes Claude Code CLI is already installed and authenticated.
It uses the same environment as the terminal - no API keys needed.
"""

import subprocess
import sys
import os
import json
import re
from typing import Optional, List, Dict, Any, Tuple
from data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
)

# Get Claude Code CLI path from environment or use default
CLAUDE_PATH = os.getenv("CLAUDE_CODE_PATH", "claude")


def check_claude_installed() -> Optional[str]:
    """Check if Claude Code CLI is installed. Return error message if not."""
    try:
        result = subprocess.run(
            [CLAUDE_PATH, "--version"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"Error: Claude Code CLI is not installed. Expected at: {CLAUDE_PATH}"
    except FileNotFoundError:
        return f"Error: Claude Code CLI is not installed. Expected at: {CLAUDE_PATH}"
    return None


def parse_jsonl_output(output_file: str) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Parse JSONL output file and return all messages and the result message.

    Returns:
        Tuple of (all_messages, result_message) where result_message is None if not found
    """
    try:
        with open(output_file, "r") as f:
            messages = [json.loads(line) for line in f if line.strip()]

            result_message = None
            for message in reversed(messages):
                if message.get("type") == "result":
                    result_message = message
                    break

            return messages, result_message
    except Exception as e:
        print(f"Error parsing JSONL file: {e}", file=sys.stderr)
        return [], None


def convert_jsonl_to_json(jsonl_file: str) -> str:
    """Convert JSONL file to JSON array file."""
    json_file = jsonl_file.replace('.jsonl', '.json')
    messages, _ = parse_jsonl_output(jsonl_file)

    with open(json_file, 'w') as f:
        json.dump(messages, f, indent=2)

    return json_file


def get_claude_env() -> Optional[Dict[str, str]]:
    """Get environment for Claude Code execution.

    Returns None to inherit the parent environment, which is what we want
    since Claude Code CLI is already authenticated on the machine.
    """
    # Return None to inherit parent environment (same as running in terminal)
    return None


def save_prompt(prompt: str, agent_id: str, agent_name: str, output_dir: str) -> Optional[str]:
    """Save a prompt to the logging directory.

    Args:
        prompt: The prompt text
        agent_id: Unique agent execution ID
        agent_name: Name of the agent
        output_dir: Base output directory

    Returns:
        Path to saved prompt file, or None if not saved
    """
    # Extract slash command from prompt
    match = re.match(r'^(/\w+)', prompt)
    if not match:
        return None

    command_name = match.group(1)[1:]  # Remove leading slash

    prompt_dir = os.path.join(output_dir, agent_id, agent_name, "prompts")
    os.makedirs(prompt_dir, exist_ok=True)

    prompt_file = os.path.join(prompt_dir, f"{command_name}.txt")
    with open(prompt_file, "w") as f:
        f.write(prompt)

    return prompt_file


def execute_prompt(request: AgentPromptRequest) -> AgentPromptResponse:
    """Execute Claude Code with the given prompt configuration.

    Args:
        request: AgentPromptRequest with prompt and configuration

    Returns:
        AgentPromptResponse with output and status
    """
    # Check if Claude Code CLI is installed
    error_msg = check_claude_installed()
    if error_msg:
        return AgentPromptResponse(output=error_msg, success=False)

    # Build command
    cmd = [CLAUDE_PATH, "-p", request.prompt]
    cmd.extend(["--model", request.model])

    # Add dangerous skip permissions flag if enabled
    if request.dangerously_skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    # Determine working directory
    cwd = request.working_directory or os.getcwd()

    # Set up environment
    env = get_claude_env()

    try:
        # If output file specified, use stream-json format
        if request.output_file:
            cmd.extend(["--output-format", "stream-json"])
            cmd.append("--verbose")

            output_dir = os.path.dirname(request.output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(request.output_file, "w") as f:
                result = subprocess.run(
                    cmd, stdout=f, stderr=subprocess.PIPE, text=True,
                    env=env, cwd=cwd
                )

            if result.returncode == 0:
                messages, result_message = parse_jsonl_output(request.output_file)
                convert_jsonl_to_json(request.output_file)

                if result_message:
                    return AgentPromptResponse(
                        output=result_message.get("result", ""),
                        success=not result_message.get("is_error", False),
                        session_id=result_message.get("session_id"),
                        cost_usd=result_message.get("total_cost_usd"),
                        duration_ms=result_message.get("duration_ms"),
                    )

            return AgentPromptResponse(
                output=f"Error: {result.stderr}",
                success=False,
            )
        else:
            # Simple text output
            cmd.extend(["--output-format", "text"])

            result = subprocess.run(
                cmd, capture_output=True, text=True, env=env, cwd=cwd
            )

            return AgentPromptResponse(
                output=result.stdout.strip() if result.returncode == 0 else result.stderr,
                success=result.returncode == 0,
            )

    except subprocess.TimeoutExpired:
        return AgentPromptResponse(
            output="Error: Claude Code command timed out",
            success=False,
        )
    except Exception as e:
        return AgentPromptResponse(
            output=f"Error executing Claude Code: {e}",
            success=False,
        )


def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a Claude Code template with slash command and arguments.

    Args:
        request: AgentTemplateRequest with command and arguments

    Returns:
        AgentPromptResponse with output and status
    """
    # Construct prompt from slash command and args
    prompt = f"{request.slash_command} {' '.join(request.args)}"

    # Determine output directory
    if request.working_directory:
        output_dir = os.path.join(request.working_directory, "agents")
    else:
        output_dir = os.path.join(os.getcwd(), "agents")

    os.makedirs(output_dir, exist_ok=True)

    # Build output file path
    output_file = os.path.join(
        output_dir, request.agent_id, request.agent_name, "raw_output.jsonl"
    )

    # Create prompt request
    prompt_request = AgentPromptRequest(
        prompt=prompt,
        agent_id=request.agent_id,
        agent_name=request.agent_name,
        model=request.model,
        dangerously_skip_permissions=True,
        output_file=output_file,
        working_directory=request.working_directory,
    )

    return execute_prompt(prompt_request)


def execute_simple(
    prompt: str,
    model: str = "sonnet",
    working_directory: Optional[str] = None,
) -> AgentPromptResponse:
    """Execute a simple prompt without file output.

    Args:
        prompt: The prompt to execute
        model: Model to use (sonnet, opus, haiku)
        working_directory: Directory to run in

    Returns:
        AgentPromptResponse with output and status
    """
    from utils import make_adw_id

    request = AgentPromptRequest(
        prompt=prompt,
        agent_id=make_adw_id(),
        agent_name="simple",
        model=model,
        working_directory=working_directory,
    )

    return execute_prompt(request)
