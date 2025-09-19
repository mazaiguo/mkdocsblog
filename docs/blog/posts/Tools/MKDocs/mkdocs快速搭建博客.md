---
title: mkdocs快速搭建博客
date: 2025-09-19
categories:
  - Python
  - 开发工具
  - Tools
tags:
  - Python
  - PyInstaller
  - 打包
  - 可执行文件
  - MkDocs
  - MarkDown
description: 使用mkdocs快速搭建博客或帮助文档
authors:
  - JerryMa
---

# mkdocs快速搭建博客

## 安装依赖

`requirement.txt`

```text
# MkDocs 核心
mkdocs>=1.5.0
mkdocs-material>=9.4.0

# 博客功能（包含在 mkdocs-material 中）
# mkdocs-blog-plugin  # 不需要单独安装

# 功能增强插件
mkdocs-minify-plugin>=0.7.0
mkdocs-glightbox>=0.3.4

# Git 相关插件（可选，需要系统安装 Git）
# mkdocs-git-revision-date-localized-plugin>=1.2.0

# 其他可选插件
# mkdocs-awesome-pages-plugin
# mkdocs-redirects
# mkdocs-rss-plugin
```

