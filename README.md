# hylreg-hub

在一个 Git 仓库中集中管理多个 Git 仓库：通过配置文件列出子仓库，用脚本批量克隆、拉取、查看状态。

## 目录结构

```
hylreg_hub/
├── repos.json          # 要管理的仓库列表（编辑此文件添加/删除仓库）
├── repos/              # 子仓库克隆到此目录（默认）
├── scripts/
│   └── manage_repos.py # 管理脚本
├── pyproject.toml
└── README.md
```

## 配置仓库列表

编辑 `repos.json`，在 `repos` 数组中添加仓库：

```json
{
  "repos": [
    {
      "name": "my-project",
      "url": "https://github.com/you/my-project.git",
      "branch": "main",
      "path": "repos/my-project"
    }
  ]
}
```

- `name`、`url` 必填；`branch` 可选，默认 `main`；`path` 可选，不写则默认为 `repos/<name>`。  
- 删除某个仓库：从数组中移除对应项即可（本地 `repos/` 里的目录需自行删除）。

## 使用方式

### 1. 用 uv 运行（推荐）

```bash
# 克隆配置中的所有仓库到 repos/
uv run python scripts/manage_repos.py clone

# 对所有已克隆的仓库执行 git pull
uv run python scripts/manage_repos.py pull

# 查看各仓库的 git status
uv run python scripts/manage_repos.py status
```

指定仓库根目录和配置文件：

```bash
uv run python scripts/manage_repos.py -C /path/to/hub clone
uv run python scripts/manage_repos.py -c /path/to/repos.json status
```

### 2. 安装后使用

```bash
uv sync
uv run manage-repos clone
uv run manage-repos pull
uv run manage-repos status
```

## 与 Git 子模块的关系

- **当前方式**：只做「配置 + 脚本」管理，子仓库是普通 clone，和本仓库的 Git 无关，适合「一堆独立项目放在一起克隆/更新」。
- 若你希望**本仓库的提交里记录每个子仓库的精确 commit**，可以用 Git 子模块：
  - 在要放子仓库的目录执行：`git submodule add <url> repos/<name>`
  - 子模块的 commit 会记录在本仓库的 `.gitmodules` 和提交里，其他人 `clone --recurse-submodules` 或 `submodule update --init` 即可拿到相同版本。

两种方式可以并存：部分用脚本管理，部分用 submodule，按需选择。
