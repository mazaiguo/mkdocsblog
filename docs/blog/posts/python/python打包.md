---
title: Python应用程序打包指南
date: 2025-09-18
categories:
  - Python
  - 开发工具
tags:
  - Python
  - PyInstaller
  - 打包
  - 可执行文件
description: 使用PyInstaller将Python脚本打包为独立可执行文件的方法和参数说明
authors:
  - JerryMa
---

# Python应用程序打包指南

使用PyInstaller将Python脚本打包为可执行文件：

```bash
pyinstaller -F -w -i 21.ico gitlog.py
```

**参数说明：**
- `-F`: 生成单个可执行文件
- `-w`: 不显示控制台窗口（适用于GUI应用）
- `-i 21.ico`: 指定应用程序图标
- `gitlog.py`: 要打包的Python脚本文件