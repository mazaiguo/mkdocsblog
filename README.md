# Jerry Ma 技术博客

使用 MkDocs Material 构建的现代化技术博客，支持标签、分类、搜索等完整的博客功能。

## 🚀 功能特性

### 博客功能
- ✅ 博客文章管理
- ✅ 标签系统
- ✅ 分类系统  
- ✅ 文章归档
- ✅ 作者信息
- ✅ 文章元数据

### 用户体验
- ✅ 响应式设计
- ✅ 深浅主题切换
- ✅ 全文搜索
- ✅ 图片放大预览
- ✅ 代码高亮
- ✅ 代码复制
- ✅ 目录导航
- ✅ 返回顶部

### 内容增强
- ✅ Markdown 扩展
- ✅ 数学公式支持
- ✅ 图表支持 (Mermaid)
- ✅ 警告框 (Admonitions)
- ✅ 标签页 (Tabs)
- ✅ 任务列表
- ✅ 脚注支持

### 性能优化
- ✅ 文件压缩
- ✅ 离线支持
- ✅ 快速导航
- ✅ 预加载

## 📁 项目结构

```
helpdoc/
├── docs/                    # 文档源文件
│   ├── blog/               # 博客相关文件
│   │   ├── .authors.yml    # 作者配置
│   │   ├── index.md        # 博客首页
│   │   └── posts/          # 博客文章
│   │       ├── CPP/        # C++ 相关文章
│   │       ├── ObjectARX.net/  # AutoCAD.NET 相关文章
│   │       └── python/     # Python 相关文章
│   ├── stylesheets/        # 自定义样式
│   │   └── extra.css       # 额外CSS样式
│   ├── index.md            # 网站首页
│   ├── tags.md             # 标签页面
│   └── about.md            # 关于页面
├── mkdocs.yml              # MkDocs 配置文件
└── README.md               # 项目说明
```

## 🛠️ 安装和使用

### 环境要求

- Python 3.7+
- pip

### 安装依赖

```bash
pip install mkdocs-material
pip install mkdocs-blog-plugin
pip install mkdocs-glightbox
pip install mkdocs-minify-plugin
pip install mkdocs-git-revision-date-localized-plugin
```

### 启动开发服务器

```bash
# 克隆项目
git clone <repository-url>
cd helpdoc

# 启动本地服务器
mkdocs serve
```

访问 `http://127.0.0.1:8000` 查看博客。

### 构建静态网站

```bash
mkdocs build
```

生成的静态文件在 `site/` 目录中。

## ✍️ 写作指南

### 创建新文章

1. 在 `docs/blog/posts/` 的相应分类目录下创建新的 Markdown 文件
2. 添加文章元数据（front matter）

```yaml
---
title: 文章标题
date: 2025-09-18
categories:
  - 分类1
  - 分类2
tags:
  - 标签1
  - 标签2
description: 文章描述
authors:
  - JerryMa
---

# 文章内容开始...
```

### 文章元数据说明

- `title`: 文章标题
- `date`: 发布日期 (YYYY-MM-DD)
- `categories`: 文章分类（列表）
- `tags`: 文章标签（列表）
- `description`: 文章描述
- `authors`: 作者列表

### 支持的 Markdown 语法

#### 代码块
```python
def hello_world():
    print("Hello, World!")
```

#### 警告框
!!! note "提示"
    这是一个提示框

!!! warning "警告"
    这是一个警告框

#### 标签页
=== "Python"
    ```python
    print("Hello Python")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello JavaScript");
    ```

#### 任务列表
- [x] 已完成任务
- [ ] 待完成任务

#### 数学公式
行内公式：$E = mc^2$

块级公式：
$$
\int_a^b f(x) dx = F(b) - F(a)
$$

## 🎨 自定义样式

### 添加自定义CSS

在 `docs/stylesheets/extra.css` 中添加自定义样式。

### 主题配置

在 `mkdocs.yml` 中可以配置：
- 主题颜色
- 字体
- 功能特性
- 插件设置

## 📋 配置说明

### 主要插件

- **blog**: 博客功能
- **tags**: 标签系统
- **search**: 搜索功能
- **minify**: 文件压缩
- **glightbox**: 图片预览
- **git-revision-date-localized**: 文章日期

### 博客配置

```yaml
- blog:
    blog_dir: blog
    post_dir: "{blog}/posts"
    categories: true
    archive: true
    pagination_per_page: 10
```

## 🚀 部署

### GitHub Pages

1. 在 GitHub 仓库中启用 Pages
2. 配置 GitHub Actions 自动部署

### 其他部署方式

- Netlify
- Vercel  
- 自建服务器

## 📝 许可证

本项目遵循 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- **GitHub**: [mazaiguo](https://github.com/mazaiguo)
- **Email**: mazaiguo@126.com

---

*使用 MkDocs Material 构建，为技术分享而生。*

