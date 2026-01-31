# hylreg-hub

使用 **Git Submodule** 在一个仓库中管理多个 Git 子仓库。本仓库的每次提交会记录各子仓库的**固定 commit**，他人 clone 后可复现同一套代码组合。

## 目录结构

```
hylreg_hub/
├── repos/              # 子模块放在此目录（每个子目录对应一个 submodule）
├── .gitmodules         # 子模块列表（由 git submodule add 自动生成）
└── README.md
```

## 添加子仓库（子模块）

在仓库根目录执行：

```bash
# 添加子模块到 repos/<名称>
git submodule add <仓库URL> repos/<名称>

# 示例
git submodule add https://github.com/example/my-project.git repos/my-project
```

添加后需要提交本仓库的变更（包含 `.gitmodules` 和 `repos/<名称>` 的 gitlink）：

```bash
git add .gitmodules repos/<名称>
git commit -m "chore: 添加子模块 repos/<名称>"
```

## 克隆本仓库（含所有子模块）

```bash
# 一次性克隆本仓库并初始化、拉取所有子模块
git clone --recurse-submodules <本仓库URL>
cd hylreg_hub
```

若已经 clone 了本仓库但当时未带子模块：

```bash
git submodule update --init --recursive
```

## 日常使用

### 拉取本仓库与所有子模块到最新

```bash
git pull
git submodule update --init --recursive
```

或只更新子模块到本仓库记录的 commit（不拉取子模块远端）：

```bash
git submodule update --init --recursive
```

### 只拉取 / 更新指定子模块

只初始化并拉取某一个子模块（到本仓库记录的 commit）：

```bash
git submodule update --init repos/<名称>
```

只把某一个子模块更新到其远端最新：

```bash
git submodule update --remote repos/<名称>
```

也可以进入该子模块目录后自己拉取：

```bash
cd repos/<名称>
git pull
cd ../..
```

若希望本仓库记录该子模块的新 commit，再执行 `git add repos/<名称>` 并提交。

### 在子模块里工作

```bash
cd repos/<名称>
git checkout main   # 或你要的分支
git pull
# 修改、提交、推送...
cd ../..
# 若希望本仓库记录该子模块的新 commit：
git add repos/<名称>
git commit -m "chore: 更新子模块 <名称>"
git push
```

### 更新子模块到其远端最新并记录到本仓库

```bash
git submodule update --remote repos/<名称>
git add repos/<名称>
git commit -m "chore: 更新子模块 <名称> 到最新"
git push
```

### 删除子模块

```bash
# 1. 反注册并移除工作区（不删子模块目录里的文件则去掉 --force）
git submodule deinit -f repos/<名称>
git rm -f repos/<名称>
# 2. 删除 .git/modules/repos/<名称>（可选，彻底清理）
rm -rf .git/modules/repos/<名称>
# 3. 提交
git commit -m "chore: 移除子模块 repos/<名称>"
```

## 查看有哪些子模块

**子模块列表在 clone 本仓库时就已经带下来了**，不需要先拉取任何子模块也能看到。

- **看配置文件**：打开根目录下的 `.gitmodules`，里面会列出每个子模块的 `path` 和 `url`。例如：
  ```ini
  [submodule "repos/my-project"]
      path = repos/my-project
      url = https://github.com/example/my-project.git
  ```
  这里的 `path` 就是子模块在本仓库里的路径（如 `repos/my-project`），拉取指定子模块时用这个路径即可。

- **用命令列出路径**：在仓库根目录执行下面命令，只打印所有子模块的路径（方便复制去拉取）：
  ```bash
  git config --file .gitmodules --get-regexp path | awk '{ print $2 }'
  ```

- **看状态**：执行下面命令会列出所有子模块及其当前 commit、是否已初始化、是否有未提交修改：
  ```bash
  git submodule status
  ```
  尚未执行过 `git submodule update --init` 时，对应子模块会显示为「未初始化」；初始化后才会显示具体 commit。

**流程**：先看 `.gitmodules` 或上面命令知道有哪些子模块（路径），再按需执行 `git submodule update --init repos/<名称>` 拉取指定子模块。

**添加 hylreg_LLM 子模块**（若尚未添加）：在仓库根目录执行  
`git submodule add https://github.com/hylreg/hylreg_LLM.git repos/hylreg_LLM`，然后提交 `.gitmodules` 和 `repos/hylreg_LLM`。
