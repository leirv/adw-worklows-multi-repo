"""Git operations module - generic git actions."""

import subprocess
import sys
import os
from typing import Optional, Tuple


def run_git_command(
    args: list,
    cwd: Optional[str] = None,
    capture_output: bool = True,
) -> Tuple[bool, str, str]:
    """Run a git command and return (success, stdout, stderr).

    Args:
        args: Git command arguments (without 'git' prefix)
        cwd: Working directory for the command
        capture_output: Whether to capture output

    Returns:
        Tuple of (success, stdout, stderr)
    """
    cmd = ["git"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            cwd=cwd,
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        return False, "", "git command not found"
    except Exception as e:
        return False, "", str(e)


# =============================================================================
# Repository Operations
# =============================================================================

def get_repo_url(cwd: Optional[str] = None) -> str:
    """Get the remote URL of the current repository.

    Args:
        cwd: Working directory (defaults to current)

    Returns:
        The remote URL

    Raises:
        ValueError: If no remote found or git not available
    """
    success, stdout, stderr = run_git_command(
        ["remote", "get-url", "origin"],
        cwd=cwd,
    )
    if not success:
        raise ValueError(f"Failed to get remote URL: {stderr}")
    return stdout


def extract_repo_path(url: str) -> str:
    """Extract owner/repo from a git URL.

    Handles:
    - https://github.com/owner/repo
    - https://github.com/owner/repo.git
    - git@github.com:owner/repo.git

    Args:
        url: The git URL

    Returns:
        The owner/repo string
    """
    # Handle SSH URLs
    if url.startswith("git@"):
        # git@github.com:owner/repo.git -> owner/repo
        url = url.split(":")[-1]

    # Handle HTTPS URLs
    url = url.replace("https://github.com/", "")
    url = url.replace("https://gitlab.com/", "")
    url = url.replace("https://bitbucket.org/", "")

    # Remove .git suffix
    if url.endswith(".git"):
        url = url[:-4]

    return url


def get_repo_name_from_url(url: str) -> str:
    """Extract just the repo name from a URL.

    Args:
        url: The git URL

    Returns:
        The repository name (without owner)
    """
    repo_path = extract_repo_path(url)
    return repo_path.split("/")[-1]


# =============================================================================
# Branch Operations
# =============================================================================

def get_current_branch(cwd: Optional[str] = None) -> str:
    """Get the current branch name.

    Args:
        cwd: Working directory

    Returns:
        Current branch name

    Raises:
        ValueError: If not in a git repo or detached HEAD
    """
    success, stdout, stderr = run_git_command(
        ["branch", "--show-current"],
        cwd=cwd,
    )
    if not success or not stdout:
        raise ValueError(f"Failed to get current branch: {stderr}")
    return stdout


def create_branch(branch_name: str, cwd: Optional[str] = None) -> bool:
    """Create and checkout a new branch.

    Args:
        branch_name: Name of the branch to create
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(
        ["checkout", "-b", branch_name],
        cwd=cwd,
    )
    if not success:
        print(f"Error creating branch: {stderr}", file=sys.stderr)
    return success


def checkout_branch(branch_name: str, cwd: Optional[str] = None) -> bool:
    """Checkout an existing branch.

    Args:
        branch_name: Name of the branch
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(
        ["checkout", branch_name],
        cwd=cwd,
    )
    if not success:
        print(f"Error checking out branch: {stderr}", file=sys.stderr)
    return success


def branch_exists(branch_name: str, cwd: Optional[str] = None) -> bool:
    """Check if a branch exists.

    Args:
        branch_name: Name of the branch
        cwd: Working directory

    Returns:
        True if branch exists
    """
    success, _, _ = run_git_command(
        ["rev-parse", "--verify", branch_name],
        cwd=cwd,
    )
    return success


# =============================================================================
# Commit Operations
# =============================================================================

def stage_all(cwd: Optional[str] = None) -> bool:
    """Stage all changes.

    Args:
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(["add", "-A"], cwd=cwd)
    if not success:
        print(f"Error staging changes: {stderr}", file=sys.stderr)
    return success


def stage_files(files: list, cwd: Optional[str] = None) -> bool:
    """Stage specific files.

    Args:
        files: List of file paths to stage
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(["add"] + files, cwd=cwd)
    if not success:
        print(f"Error staging files: {stderr}", file=sys.stderr)
    return success


def commit(message: str, cwd: Optional[str] = None) -> bool:
    """Create a commit with the given message.

    Args:
        message: Commit message
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(
        ["commit", "-m", message],
        cwd=cwd,
    )
    if not success:
        print(f"Error committing: {stderr}", file=sys.stderr)
    return success


def get_diff_stat(cwd: Optional[str] = None) -> str:
    """Get diff statistics for staged changes.

    Args:
        cwd: Working directory

    Returns:
        Diff stat output
    """
    success, stdout, _ = run_git_command(
        ["diff", "--stat", "--cached"],
        cwd=cwd,
    )
    return stdout if success else ""


# =============================================================================
# Submodule Operations
# =============================================================================

def add_submodule(url: str, path: str, cwd: Optional[str] = None) -> bool:
    """Add a git submodule.

    Args:
        url: Repository URL to add
        path: Path where to add the submodule
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(
        ["submodule", "add", url, path],
        cwd=cwd,
    )
    if not success:
        print(f"Error adding submodule: {stderr}", file=sys.stderr)
    return success


def remove_submodule(path: str, cwd: Optional[str] = None) -> bool:
    """Remove a git submodule.

    Args:
        path: Path of the submodule to remove
        cwd: Working directory

    Returns:
        True if successful
    """
    # Deinit the submodule
    success, _, stderr = run_git_command(
        ["submodule", "deinit", "-f", path],
        cwd=cwd,
    )
    if not success:
        print(f"Error deinitializing submodule: {stderr}", file=sys.stderr)
        return False

    # Remove from .git/modules
    success, _, stderr = run_git_command(
        ["rm", "-f", path],
        cwd=cwd,
    )
    if not success:
        print(f"Error removing submodule: {stderr}", file=sys.stderr)
        return False

    return True


def init_submodules(cwd: Optional[str] = None) -> bool:
    """Initialize all submodules.

    Args:
        cwd: Working directory

    Returns:
        True if successful
    """
    success, _, stderr = run_git_command(
        ["submodule", "update", "--init", "--recursive"],
        cwd=cwd,
    )
    if not success:
        print(f"Error initializing submodules: {stderr}", file=sys.stderr)
    return success


def list_submodules(cwd: Optional[str] = None) -> list:
    """List all submodules.

    Args:
        cwd: Working directory

    Returns:
        List of submodule paths
    """
    success, stdout, _ = run_git_command(
        ["submodule", "status"],
        cwd=cwd,
    )
    if not success or not stdout:
        return []

    submodules = []
    for line in stdout.split("\n"):
        if line.strip():
            # Format: " <hash> <path> (<branch>)" or "-<hash> <path>"
            parts = line.strip().split()
            if len(parts) >= 2:
                # The path is the second part (first might be hash with prefix)
                path = parts[1]
                submodules.append(path)

    return submodules


# =============================================================================
# Push/Pull Operations
# =============================================================================

def push(
    remote: str = "origin",
    branch: Optional[str] = None,
    set_upstream: bool = False,
    cwd: Optional[str] = None,
) -> bool:
    """Push changes to remote.

    Args:
        remote: Remote name
        branch: Branch name (None = current branch)
        set_upstream: Whether to set upstream tracking
        cwd: Working directory

    Returns:
        True if successful
    """
    args = ["push"]
    if set_upstream:
        args.append("-u")
    args.append(remote)
    if branch:
        args.append(branch)

    success, _, stderr = run_git_command(args, cwd=cwd)
    if not success:
        print(f"Error pushing: {stderr}", file=sys.stderr)
    return success


def pull(
    remote: str = "origin",
    branch: Optional[str] = None,
    cwd: Optional[str] = None,
) -> bool:
    """Pull changes from remote.

    Args:
        remote: Remote name
        branch: Branch name (None = current branch)
        cwd: Working directory

    Returns:
        True if successful
    """
    args = ["pull", remote]
    if branch:
        args.append(branch)

    success, _, stderr = run_git_command(args, cwd=cwd)
    if not success:
        print(f"Error pulling: {stderr}", file=sys.stderr)
    return success


# =============================================================================
# Status Operations
# =============================================================================

def get_status(cwd: Optional[str] = None) -> str:
    """Get git status output.

    Args:
        cwd: Working directory

    Returns:
        Status output
    """
    success, stdout, _ = run_git_command(["status"], cwd=cwd)
    return stdout if success else ""


def has_changes(cwd: Optional[str] = None) -> bool:
    """Check if there are uncommitted changes.

    Args:
        cwd: Working directory

    Returns:
        True if there are changes
    """
    success, stdout, _ = run_git_command(
        ["status", "--porcelain"],
        cwd=cwd,
    )
    return bool(stdout.strip())
