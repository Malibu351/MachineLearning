#!/bin/bash

# VSCode 工作区配置自动设置脚本
# 使用方法: ./setup_vscode_config.sh [项目路径]

PROJECT_PATH=${1:-.}

echo "正在为项目 $PROJECT_PATH 设置VSCode配置..."

# 创建.vscode目录
mkdir -p "$PROJECT_PATH/.vscode"

# 创建settings.json
cat > "$PROJECT_PATH/.vscode/settings.json" << 'EOF'
{
    "terminal.integrated.cwd": "${workspaceFolder}",
    "python.terminal.activateEnvironment": true,
    "python.defaultInterpreterPath": "python3",
    "files.exclude": {
        "**/.git": true,
        "**/.DS_Store": true,
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "search.exclude": {
        "**/.git": true,
        "**/node_modules": true,
        "**/bower_components": true,
        "**/*.code-search": true
    }
}
EOF

# 创建launch.json
cat > "$PROJECT_PATH/.vscode/launch.json" << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: Current File (External Terminal)",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "externalTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
EOF

# 创建tasks.json
cat > "$PROJECT_PATH/.vscode/tasks.json" << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Python File",
            "type": "shell",
            "command": "python",
            "args": ["${file}"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "options": {
                "cwd": "${workspaceFolder}"
            }
        },
        {
            "label": "Run Current Directory",
            "type": "shell",
            "command": "python",
            "args": ["-m", "pytest"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "options": {
                "cwd": "${workspaceFolder}"
            }
        }
    ]
}
EOF

# 创建工作区文件
PROJECT_NAME=$(basename "$(realpath "$PROJECT_PATH")")
cat > "$PROJECT_PATH/${PROJECT_NAME}.code-workspace" << EOF
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "terminal.integrated.cwd": "\${workspaceFolder}",
        "python.terminal.activateEnvironment": true,
        "python.defaultInterpreterPath": "python3",
        "files.exclude": {
            "**/.git": true,
            "**/.DS_Store": true,
            "**/__pycache__": true,
            "**/*.pyc": true
        },
        "search.exclude": {
            "**/.git": true,
            "**/node_modules": true,
            "**/bower_components": true,
            "**/*.code-search": true
        }
    },
    "extensions": {
        "recommendations": [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-vscode.vscode-json"
        ]
    }
}
EOF

echo "✅ VSCode配置设置完成！"
echo "📁 配置文件位置: $PROJECT_PATH/.vscode/"
echo "🔧 工作区文件: $PROJECT_PATH/${PROJECT_NAME}.code-workspace"
echo ""
echo "💡 使用方法:"
echo "1. 双击 ${PROJECT_NAME}.code-workspace 文件打开工作区"
echo "2. 或者使用 File > Open Workspace from File... 选择该文件"
echo "3. 现在运行代码时，工作目录将自动设置为当前项目根目录"