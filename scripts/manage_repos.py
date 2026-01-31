#!/usr/bin/env python3
"""管理多个 Git 仓库：克隆、拉取、状态。"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_config(config_path: Path) -> list[dict]:
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("repos", [])


def repo_path(base: Path, repo: dict) -> Path:
    path = repo.get("path")
    if path:
        return base / path
    return base / "repos" / repo["name"]


def run_git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def cmd_clone(base: Path, repos: list[dict]) -> None:
    base_repos = base / "repos"
    base_repos.mkdir(parents=True, exist_ok=True)
    for repo in repos:
        dest = repo_path(base, repo)
        if (dest / ".git").exists():
            print(f"跳过（已存在）: {repo['name']} -> {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        branch = repo.get("branch", "main")
        r = run_git(base, "clone", "-b", branch, "--", repo["url"], str(dest))
        if r.returncode != 0:
            print(f"克隆失败 {repo['name']}: {r.stderr or r.stdout}", file=sys.stderr)
        else:
            print(f"已克隆: {repo['name']} -> {dest}")


def cmd_pull(base: Path, repos: list[dict]) -> None:
    for repo in repos:
        dest = repo_path(base, repo)
        if not (dest / ".git").exists():
            print(f"跳过（未克隆）: {repo['name']} -> {dest}")
            continue
        r = run_git(dest, "pull")
        if r.returncode != 0:
            print(f"拉取失败 {repo['name']}: {r.stderr or r.stdout}", file=sys.stderr)
        else:
            print(f"已拉取: {repo['name']}")


def cmd_status(base: Path, repos: list[dict]) -> None:
    for repo in repos:
        dest = repo_path(base, repo)
        if not (dest / ".git").exists():
            print(f"未克隆: {repo['name']} -> {dest}")
            continue
        r = run_git(dest, "status", "-sb")
        branch = repo.get("branch", "main")
        print(f"--- {repo['name']} ({branch}) ---")
        print(r.stdout or r.stderr or "(无输出)")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="管理多个 Git 仓库")
    parser.add_argument(
        "command",
        choices=["clone", "pull", "status"],
        help="clone=克隆全部, pull=拉取全部, status=查看状态",
    )
    parser.add_argument(
        "-C", "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="仓库根目录（默认当前目录）",
    )
    parser.add_argument(
        "-c", "--config",
        type=Path,
        default=None,
        help="配置文件路径（默认 <repo-root>/repos.json）",
    )
    args = parser.parse_args()

    base = args.repo_root.resolve()
    config_path = args.config or (base / "repos.json")
    if not config_path.is_file():
        print(f"配置文件不存在: {config_path}", file=sys.stderr)
        sys.exit(1)

    repos = load_config(config_path)
    if not repos:
        print("repos.json 中未配置任何仓库。", file=sys.stderr)
        sys.exit(0)

    if args.command == "clone":
        cmd_clone(base, repos)
    elif args.command == "pull":
        cmd_pull(base, repos)
    else:
        cmd_status(base, repos)


if __name__ == "__main__":
    main()
