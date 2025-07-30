#!/usr/bin/env python3
"""
测试VSCode工作区配置是否正确
"""

import os
import sys

def test_workspace_config():
    """测试工作区配置"""
    print("=" * 50)
    print("VSCode 工作区配置测试")
    print("=" * 50)
    
    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 获取Python路径
    python_path = os.environ.get('PYTHONPATH', '')
    print(f"PYTHONPATH: {python_path}")
    
    # 获取系统路径
    print(f"Python系统路径:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    # 检查是否在git仓库中
    git_dir = os.path.join(current_dir, '.git')
    if os.path.exists(git_dir):
        print(f"✅ 当前目录是git仓库")
    else:
        print(f"⚠️  当前目录不是git仓库")
    
    # 检查是否有.vscode目录
    vscode_dir = os.path.join(current_dir, '.vscode')
    if os.path.exists(vscode_dir):
        print(f"✅ 找到.vscode配置目录")
        
        # 检查配置文件
        config_files = ['settings.json', 'launch.json', 'tasks.json']
        for config_file in config_files:
            config_path = os.path.join(vscode_dir, config_file)
            if os.path.exists(config_path):
                print(f"  ✅ {config_file}")
            else:
                print(f"  ❌ {config_file}")
    else:
        print(f"❌ 未找到.vscode配置目录")
    
    # 检查工作区文件
    workspace_files = [f for f in os.listdir(current_dir) if f.endswith('.code-workspace')]
    if workspace_files:
        print(f"✅ 找到工作区文件: {workspace_files}")
    else:
        print(f"❌ 未找到工作区文件")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    test_workspace_config()