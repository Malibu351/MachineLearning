# VSCode 工作区配置说明

## 问题描述
在VSCode中通过SSH远程连接工作区时，当有多个git项目时，默认工作目录可能不是当前git项目的根目录，导致相对路径导入和文件路径出现问题。

## 解决方案

### 1. 使用工作区文件（推荐）
- 双击 `workspace.code-workspace` 文件打开工作区
- 或者通过 `File > Open Workspace from File...` 选择该文件

### 2. 配置文件说明

#### `.vscode/settings.json`
- `terminal.integrated.cwd`: 设置终端默认工作目录为当前工作区文件夹
- `python.terminal.activateEnvironment`: 自动激活Python虚拟环境
- `python.defaultInterpreterPath`: 设置默认Python解释器

#### `.vscode/launch.json`
- 配置调试器启动时使用正确的工作目录
- 设置 `PYTHONPATH` 环境变量为工作区根目录

#### `.vscode/tasks.json`
- 配置任务运行时使用正确的工作目录
- 提供常用的Python运行和测试任务

### 3. 使用方法

#### 运行Python文件
1. 打开要运行的Python文件
2. 按 `F5` 或使用调试面板运行
3. 或者按 `Ctrl+Shift+P` 运行任务

#### 在终端中运行
1. 打开集成终端 (`Ctrl+`` `)
2. 终端会自动切换到当前工作区目录
3. 直接运行Python命令

#### 切换项目
1. 关闭当前工作区
2. 打开新的git项目目录
3. 使用 `File > Open Folder...` 打开新项目
4. 或者复制这些配置文件到新项目中

### 4. 环境变量设置
确保 `PYTHONPATH` 包含当前项目根目录，这样Python就能正确找到模块：
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 5. 验证配置
运行以下命令验证工作目录是否正确：
```python
import os
print("当前工作目录:", os.getcwd())
print("Python路径:", os.environ.get('PYTHONPATH', ''))
```

## 注意事项
- 每个git项目都需要这些配置文件
- 可以通过脚本自动复制这些配置文件到新项目中
- 如果使用虚拟环境，确保在settings.json中指定正确的Python解释器路径