#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VS Code GitHub Copilot Claude-3.7模型支持修复工具

这个脚本可以自动修改GitHub Copilot Chat插件，使其支持claude-3.7模型。
根据博客文章：https://blog.csdn.net/eieihihi/article/details/146296925 的解决方案实现。
"""

import os
import re
import platform
import shutil
import glob
from pathlib import Path
import sys

def get_extension_path():
    """获取VS Code扩展文件夹路径"""
    system = platform.system()
    home = Path.home()
    
    if system == "Windows":
        return home / ".vscode" / "extensions"
    elif system in ["Darwin", "Linux"]:  # macOS或Linux
        return home / ".vscode" / "extensions"
    else:
        print(f"不支持的操作系统: {system}")
        sys.exit(1)

def find_copilot_chat_extension(ext_path):
    """查找GitHub Copilot Chat扩展文件夹"""
    pattern = "github.copilot-chat-*"
    matches = list(ext_path.glob(pattern))
    
    if not matches:
        print("未找到GitHub Copilot Chat扩展。请确保已安装此扩展。")
        sys.exit(1)
    
    # 如果有多个版本，选择最新的
    return sorted(matches, key=lambda x: os.path.getmtime(x), reverse=True)[0]

def backup_file(file_path):
    """备份原始文件"""
    backup_path = str(file_path) + ".backup"
    shutil.copy2(file_path, backup_path)
    print(f"原始文件已备份到: {backup_path}")
    return backup_path

def modify_extension_js(ext_folder):
    """修改extension.js文件，移除x-onbehalf-extension-id头信息"""
    extension_js_path = ext_folder / "dist" / "extension.js"
    
    if not extension_js_path.exists():
        print(f"未找到extension.js文件: {extension_js_path}")
        sys.exit(1)
    
    # 备份原始文件
    backup_file(extension_js_path)
    
    # 读取文件内容
    with open(extension_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并移除特定头信息代码
    # 正则表达式匹配"x-onbehalf-extension-id"相关代码
    pattern = r'("x-onbehalf-extension-id"\s*:\s*`\${A}\/\${c}`\s*,?)'
    modified_content = re.sub(pattern, '', content)
    
    # 检查是否成功修改
    if modified_content == content:
        print("警告: 未找到需要修改的代码，可能扩展版本已更新或已被修改。")
        return False
    
    # 写入修改后的内容
    with open(extension_js_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    return True

def main():
    """主函数"""
    print("开始修复VS Code中GitHub Copilot Chat对claude-3.7模型的支持问题...")
    
    try:
        # 获取VS Code扩展路径
        ext_path = get_extension_path()
        print(f"VS Code扩展路径: {ext_path}")
        
        # 查找GitHub Copilot Chat扩展
        copilot_ext = find_copilot_chat_extension(ext_path)
        print(f"找到GitHub Copilot Chat扩展: {copilot_ext}")
        
        # 修改extension.js文件
        success = modify_extension_js(copilot_ext)
        
        if success:
            print("\n修复成功！请重启VS Code以使更改生效。")
            print("\n注意事项:")
            print("1. 如果修复后仍然无法使用claude-3.7模型，请确保您已经正确设置了API密钥。")
            print("2. 如果GitHub Copilot Chat扩展更新，您可能需要重新运行此脚本。")
            print("3. 如需恢复原始设置，请将备份文件重命名回原始文件名。")
        else:
            print("\n修复未完成。请参考博客文章手动修改: https://blog.csdn.net/eieihihi/article/details/146296925")
            
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()