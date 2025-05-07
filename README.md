# VS Code GitHub Copilot Claude-3.7 支持修复工具

这个工具可以自动修复VS Code中GitHub Copilot Chat对Claude-3.7模型的支持问题。

## 问题背景

在VS Code中使用Cline、Roo Code等插件时，尝试切换到Claude-3.7模型可能会遇到以下错误：

```
API 请求失败
请求失败： 400 {"error":{"message":"此请求不支持模型","param":"model","code":"model_not_supported","type":"invalid_request_error"}}
```

这个问题是由GitHub Copilot Chat在发送API请求时包含了特定的头信息（x-onbehalf-extension-id）导致的，使API服务器拒绝了对Claude-3.7模型的支持。

## 解决方案

本脚本通过自动修改GitHub Copilot Chat插件的`extension.js`文件，移除导致问题的头信息，从而解决Claude-3.7模型不支持的问题。

## 使用方法

1. 确保已安装Python 3
2. 克隆此仓库或下载脚本
3. 在终端中运行：

```bash
python3 fix_copilot_claude_support.py
```

4. 脚本执行完成后，重启VS Code以使更改生效

## 功能特点

- 自动查找VS Code扩展目录下的GitHub Copilot Chat扩展
- 备份原始文件，确保可以在需要时恢复
- 自动修改问题代码
- 提供详细的执行日志和错误处理
- 支持Windows、macOS和Linux系统

## 注意事项

1. 脚本会自动备份原始文件，备份文件名为`extension.js.backup`
2. 如果GitHub Copilot Chat扩展更新，可能需要重新运行此脚本
3. 如需恢复原始设置，请将备份文件重命名回原始文件名

## 参考

本工具基于博客文章：[解决 VS Code 中 GitHub Copilot Chat 遇到的 `claude-3.7` 模型不支持问题](https://blog.csdn.net/eieihihi/article/details/146296925)

## 许可

MIT