"""
resolve_evidence_link.py — DSLC evidence-location resolver

Safely resolves a project evidence file to a stable GitHub URL only when the
link can be proven from the Git repository that actually contains that file.
Otherwise returns a verified path or "Location not available".
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote


def _run_git(repo_or_workspace: Path, *args: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_or_workspace), *args],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, ""
    return result.returncode == 0, result.stdout.strip()


def _normalise_github_remote(remote: str) -> str | None:
    """Return https://github.com/<owner>/<repo> for recognised GitHub remotes."""
    remote = remote.strip()
    patterns = [
        r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$",
        r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$",
        r"^ssh://git@github\.com/([^/]+)/([^/]+?)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, remote, flags=re.IGNORECASE)
        if match:
            owner, repo = match.group(1), match.group(2)
            return f"https://github.com/{owner}/{repo}"
    return None


def resolve_evidence_location(file_path: Path, workspace: Path) -> dict[str, str | bool]:
    """
    Resolve an evidence file to the safest verifiable location.

    Important: repository discovery starts from the evidence file's own folder,
    not from the DSLC agent repository. This makes the resolver reusable when a
    Data Scientist's project evidence lives in a different Git repository.
    """
    workspace = workspace.resolve()
    file_path = ((workspace / file_path).resolve() if not file_path.is_absolute() else file_path.resolve())

    if not file_path.exists() or not file_path.is_file():
        return {
            "status": "not_found",
            "verified": False,
            "path": str(file_path),
            "display": "Location not available",
            "url": "",
            "reason": "Evidence file does not exist at the supplied path.",
        }

    # Discover Git from the evidence file itself.
    ok, repo_root_text = _run_git(file_path.parent, "rev-parse", "--show-toplevel")
    if not ok or not repo_root_text:
        try:
            display_path = file_path.relative_to(workspace).as_posix()
        except ValueError:
            display_path = str(file_path)
        return {
            "status": "local_only",
            "verified": True,
            "path": display_path,
            "display": display_path,
            "url": "",
            "reason": "Evidence file exists, but it is not contained in a verifiable Git repository.",
        }

    repo_root = Path(repo_root_text).resolve()
    try:
        relative_path = file_path.relative_to(repo_root)
    except ValueError:
        return {
            "status": "local_only",
            "verified": True,
            "path": str(file_path),
            "display": str(file_path),
            "url": "",
            "reason": "Evidence file exists but its repository-relative location could not be verified.",
        }

    rel_posix = relative_path.as_posix()

    # Untracked/uncommitted files never receive a GitHub URL.
    committed, _ = _run_git(repo_root, "cat-file", "-e", f"HEAD:{rel_posix}")
    if not committed:
        return {
            "status": "relative_path",
            "verified": True,
            "path": rel_posix,
            "display": rel_posix,
            "url": "",
            "reason": "Evidence file exists locally but is not present in the current committed HEAD.",
        }

    # Do not link to GitHub when the local evidence differs from the committed copy.
    unchanged, _ = _run_git(repo_root, "diff", "--quiet", "HEAD", "--", rel_posix)
    if not unchanged:
        return {
            "status": "relative_path",
            "verified": True,
            "path": rel_posix,
            "display": rel_posix,
            "url": "",
            "reason": "Evidence file has local changes that are not represented by the committed GitHub version.",
        }

    remote_ok, remote = _run_git(repo_root, "remote", "get-url", "origin")
    github_base = _normalise_github_remote(remote) if remote_ok else None
    if not github_base:
        return {
            "status": "relative_path",
            "verified": True,
            "path": rel_posix,
            "display": rel_posix,
            "url": "",
            "reason": "Repository origin is missing or is not a recognised github.com remote.",
        }

    sha_ok, commit_sha = _run_git(repo_root, "rev-parse", "HEAD")
    if not sha_ok or not re.fullmatch(r"[0-9a-fA-F]{40}", commit_sha):
        return {
            "status": "relative_path",
            "verified": True,
            "path": rel_posix,
            "display": rel_posix,
            "url": "",
            "reason": "Could not verify the current Git commit.",
        }

    encoded_path = quote(rel_posix, safe="/")
    url = f"{github_base}/blob/{commit_sha}/{encoded_path}"
    return {
        "status": "github_link",
        "verified": True,
        "path": rel_posix,
        "display": "Open in GitHub",
        "url": url,
        "reason": "Evidence file, containing Git repository, committed version, commit SHA and GitHub origin were verified locally.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve an evidence file to a verified GitHub link when possible.")
    parser.add_argument("file", help="Evidence file path, relative to --workspace unless absolute")
    parser.add_argument("--workspace", default=".", help="Workspace directory used to resolve relative input paths")
    parser.add_argument("--markdown", action="store_true", help="Return Markdown suitable for the Evidence Register")
    parser.add_argument("--json", action="store_true", help="Return structured JSON")
    args = parser.parse_args()

    result = resolve_evidence_location(Path(args.file), Path(args.workspace))
    if args.json:
        print(json.dumps(result, indent=2))
    elif args.markdown:
        if result["status"] == "github_link":
            print(f"[Open in GitHub]({result['url']})")
        elif result["status"] in {"relative_path", "local_only"}:
            print(result["display"])
        else:
            print("Location not available")
    else:
        print(f"Status : {result['status']}")
        print(f"Path   : {result['path']}")
        print(f"URL    : {result['url'] or '(none)'}")
        print(f"Reason : {result['reason']}")


if __name__ == "__main__":
    main()