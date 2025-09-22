---
title: mkdocs快速搭建博客
date: 2025-09-19
categories:
  - 开发工具
  - Tools
tags:
  - Python
  - PyInstaller
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
mkdocs-awesome-pages-plugin
# mkdocs-redirects
# mkdocs-rss-plugin
```

## yaml文件配置

`mkdoc.yml`

??? note "mkdoc.yml"
	```yaml
    site_name: 我的帮助文档
    site_description: 关于mkdocs-material支持的markdown语法，包括传统语法和扩展语法
    site_author: JerryMa
    site_url: http://127.0.0.1:8000

    repo_name: 'mkdocsblog'
    repo_url: 'https://github.com/mazaiguo/mkdocsblog'
    theme:
      name: material
      palette:
        # Toggle light mode
        - scheme: default
          primary: Blue Grey
          accent: Pink
          toggle:
            icon: material/toggle-switch
            name: 切换到明亮模式
        # Toggle dark mode
        - scheme: slate
          primary: blue
          accent: amber
          toggle:
            icon: material/toggle-switch-off-outline
            name: 切换到暗黑模式
      features:
        - announce.dismiss
        - content.tabs.link
        - content.tooltips
        - content.code.copy #代码复制
        - content.code.select
        - content.code.annotate   
        - content.footnote.tooltips
        - header.autohide
        - navigation.footer
        - navigation.indexes
        - navigation.instant
        - navigation.instant.prefetch
        - navigation.instant.progress
        - navigation.prune
        - navigation.sections
        - navigation.tabs
        - navigation.tabs.sticky
        - navigation.top # 返回顶部的按钮 在上滑时出现  
        - navigation.tracking
        - search.highlight # 搜索出的文章关键词加入高亮
        - search.share #搜索分享按钮   
        - search.suggest # 搜索输入一些字母时推荐补全整个单词
        - toc.follow
        - toc.integrate
      language: 'zh'
    plugins:
      - macros
      - blog:
          blog_dir: blog
          post_dir: "{blog}/posts"
          post_date_format: full
          post_url_format: "{date}/{slug}"
          pagination_per_page: 10
          pagination_url_format: "page/{page}"
          authors_file: "{blog}/.authors.yml"
          blog_toc: true
          categories_toc: true
          archive: true
          archive_name: 归档
          archive_date_format: "YYYY年MM月"
          archive_url_format: "archive/{date}"
          archive_toc: true
          archive_file: "archive/index.md"
          categories: true
          categories_name: 分类
          categories_url_format: "category/{slug}"
          categories_slugify: !!python/object/apply:pymdownx.slugs.slugify
            kwds:
              case: lower
      - offline
      - tags:
          tags_hierarchy: true
          tags_slugify_format: "tag:{slug}"
          tags_slugify: !!python/object/apply:pymdownx.slugs.slugify
            kwds:
              case: lower
      - search:
          lang: 
            - zh
            - en
          separator: '[\s\-\.]+'
      - minify:
          minify_html: true
          minify_js: true
          minify_css: true
          htmlmin_opts:
            remove_comments: true
          css_files:
            - stylesheets/extra.css
      - glightbox:
          touchNavigation: true
          loop: false
          effect: zoom
          slide_effect: slide
          width: 100%
          height: auto
          zoomable: true
          draggable: true
          skip_classes:
            - custom-skip-class-name
          auto_caption: false
          caption_position: bottom
      # 注释掉 git 插件，因为需要系统安装 Git
      # - git-revision-date-localized:
      #     enable_creation_date: true
      #     type: timeago
      #     locale: zh
      #     fallback_to_build_date: false
      #     exclude:
      #       - index.md
      #       - tags.md
      #       - blog/index.md
    extra:
      social:
        - icon: fontawesome/brands/github #联系方式图标 : https://fontawesome.com/ 去这里找图标
          link: https://github.com/mazaiguo
          name: JerryMa on Github
        - icon: fontawesome/brands/gitlab
          link: https://gitlab.zwsoft.cn/mazaiguo
        - icon: fontawesome/regular/envelope
          link: mailto:mazaiguo@126.com
          name: Email
      analytics:
        feedback:
          title: 这个页面对您有帮助吗？
          ratings:
            - icon: material/emoticon-happy-outline
              name: 有帮助
              data: 1
              note: >-
                感谢您的反馈！
            - icon: material/emoticon-sad-outline
              name: 可以改进
              data: 0
              note: >-
                感谢您的反馈！请帮助我们改进这个页面，
                <a href="https://github.com/mazaiguo/mazaiguo.github.io/issues/new/?title=[Feedback]+{title}+-+{url}" target="_blank" rel="noopener">告诉我们需要改进的地方</a>。
      tags:
        HTML5: html
        JavaScript: js
        CSS: css
        Python: python
        AutoCAD: autocad
        C++: cpp
        "Csharp": csharp
        ".NET": dotnet
      generator: false #是否删除页脚显示"使用 MkDocs 材料制造"
    #extra_javascript:
      #- https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js
      #- javascripts/config.js
    extra_css:
      #- https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/default.min.css
      - stylesheets/extra.css  
    markdown_extensions:
      - abbr
      - admonition
      - attr_list
      - def_list
      - footnotes
      - md_in_html
      - meta
      - toc:
          permalink: true
          title: 目录
      - pymdownx.arithmatex:
          generic: true
      - pymdownx.betterem:
          smart_enable: all
      - pymdownx.caret
      - pymdownx.details
      - pymdownx.emoji:
          emoji_generator: !!python/name:material.extensions.emoji.to_svg
          emoji_index: !!python/name:material.extensions.emoji.twemoji
      - pymdownx.highlight:
          anchor_linenums: true
          line_spans: __span
          pygments_lang_class: true
          linenums: true
          linenums_style: pymdownx.inline
          auto_title: true # 显示编程语言名称
          use_pygments: true
      - pymdownx.inlinehilite
      - pymdownx.keys
      - pymdownx.magiclink:
          normalize_issue_symbols: true
          repo_url_shorthand: true
          user: mazaiguo
          repo: helpdoc
      - pymdownx.mark
      - pymdownx.smartsymbols
      - pymdownx.snippets:
          check_paths: true
      - pymdownx.superfences:
          custom_fences:
            - name: mermaid
              class: mermaid
              format: !!python/name:pymdownx.superfences.fence_code_format
      - pymdownx.tabbed:
          alternate_style: true
          combine_header_slug: true
          slugify: !!python/object/apply:pymdownx.slugs.slugify
            kwds:
              case: lower
      - pymdownx.tasklist:
          custom_checkbox: true
      - pymdownx.tilde
      - pymdownx.critic
    copyright: Copyright &copy; 2016 - present [JerryMa](https://github.com/mazaiguo)
    nav:
      - 首页: index.md
      - 博客:
         - blog/index.md
      - 归档: archive/index.md
      - 分类: blog/category.md
      - 标签: tags.md
      - 关于: 
         - 关于本站: about.md
    ```


## 增加latex

```bash
$$
\cos x=\sum_{k=0}^{\infty}\frac{(-1)^k}{(2k)!}x^{2k}
$$
```

$$ \cos x=\sum_{k=0}^{\infty}\frac{(-1)^k}{(2k)!}x^{2k} $$

```bash
The homomorphism $f$ is injective if and only if its kernel is only the
singleton set $e_G$, because otherwise $\exists a,b\in G$ with $a\neq b$ such
that $f(a)=f(b)$.
```

The homomorphism $f$ is injective if and only if its kernel is only the singleton set $e_G$, because otherwise $\exists a,b\in G$ with $a\neq b$ such that $f(a)=f(b)$.



## contents tab

=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

=== "C++"

 ```cpp
#include <iostream>

int main(void) {
  std::cout << "Hello world!" << std::endl;
  return 0;
}
 ```

=== "c"

```c
#include <stdio.h>

int main(void) {
  printf("Hello world!\n");
  return 0;
}
```


## **Admonition**

!!! note "Outer Note"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    
    !!! note "Inner Note"
    
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
        nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
        massa, nec semper lorem quam in massa.
!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
## 特殊数据处理

`archive/index.md`

`tags.md`

不识别[TAGS]、[ARCHIVE]，用main.py中定义的自定义宏来处理

`main.py`

```python
"""
MkDocs macros for auto-generating archive content
"""
import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def define_env(env):
    """
    Define macros for MkDocs  
    """
    
    @env.macro  
    def auto_archive():
        """
        Automatically generate archive content from blog posts
        从md文件中完全自动获取所有信息，无硬编码
        """
        try:
            blog_posts_dir = Path("docs/blog/posts")
            if not blog_posts_dir.exists():
                return "## ❌ 错误\n\n无法找到博客文章目录\n\n"
            
            posts = []
            all_categories = set()  # 收集所有出现的分类
            debug_info = []  # 添加调试信息
            
            # 遍历所有文章文件
            for md_file in blog_posts_dir.rglob("*.md"):
                debug_info.append(f"处理文件: {md_file}")
                try:
                    with open(md_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    debug_info.append(f"成功读取: {md_file.name}")
                    
                    # 提取front matter
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            front_matter_text = parts[1].strip()
                            try:
                                # 解析YAML front matter
                                front_matter = yaml.safe_load(front_matter_text)
                                if not front_matter:
                                    continue
                                
                                title = front_matter.get('title', md_file.stem)
                                date = front_matter.get('date', '2025-09-18')
                                categories = front_matter.get('categories', [])
                                
                                # 确定主分类 - 完全从front matter获取
                                if isinstance(categories, list) and categories:
                                    main_category = categories[0]
                                    # 收集所有分类
                                    for cat in categories:
                                        all_categories.add(str(cat))
                                else:
                                    # 如果没有分类，跳过这篇文章或使用未分类
                                    main_category = "未分类"
                                    all_categories.add("未分类")
                                
                                # 生成相对路径
                                relative_path = os.path.relpath(md_file, Path("docs/archive")).replace('\\', '/')
                                
                                posts.append({
                                    'title': title,
                                    'date': str(date),
                                    'category': str(main_category),
                                    'path': relative_path,
                                    'all_categories': categories if isinstance(categories, list) else [main_category]
                                })
                                
                            except yaml.YAMLError as e:
                                # YAML解析失败，尝试提取基本信息
                                posts.append({
                                    'title': md_file.stem,
                                    'date': '2025-09-18', 
                                    'category': "解析失败",
                                    'path': os.path.relpath(md_file, Path("docs/archive")).replace('\\', '/'),
                                    'all_categories': ["解析失败"]
                                })
                                all_categories.add("解析失败")
                    
                except Exception as e:
                    # 文件读取失败
                    continue
            
            # 添加调试输出
            debug_text = "\n".join(debug_info[:10])  # 显示前10行调试信息
            
            if not posts:
                return f"## 📝 调试信息\n\n找到 {len(posts)} 篇文章\n\n调试:\n```\n{debug_text}\n```\n\n分类: {list(all_categories)}\n\n"
            
            # 生成干净的结果，不包含调试信息
            
            # 动态生成分类名称映射
            category_display_names = {}
            for category in all_categories:
                cat_lower = category.lower()
                if cat_lower == 'cpp' or 'c++' in cat_lower:
                    category_display_names[category] = 'C++开发'
                elif cat_lower == 'python' or 'python' in cat_lower:
                    category_display_names[category] = 'Python开发'
                elif 'autocad' in cat_lower or 'cad' in cat_lower:
                    category_display_names[category] = 'AutoCAD开发'
                elif cat_lower == 'csharp' or 'Csharp' in cat_lower or '.net' in cat_lower:
                    category_display_names[category] = 'Csharp/.NET开发'
                elif '开发工具' in category or '工具' in category:
                    category_display_names[category] = '开发工具'
                elif '未分类' in category:
                    category_display_names[category] = '未分类'
                elif '解析失败' in category:
                    category_display_names[category] = '解析失败'
                else:
                    # 默认添加"开发"后缀，除非已经包含
                    if '开发' not in category:
                        category_display_names[category] = f'{category}开发'
                    else:
                        category_display_names[category] = category
            
            # 按日期分组
            posts.sort(key=lambda x: x['date'], reverse=True)
            date_groups = defaultdict(list)
            
            for post in posts:
                try:
                    if isinstance(post['date'], str):
                        date_obj = datetime.strptime(post['date'], '%Y-%m-%d')
                    else:
                        date_obj = post['date']
                    month_key = date_obj.strftime('%Y年%m月')
                    date_groups[month_key].append(post)
                except:
                    # 日期解析失败，使用默认
                    date_groups['2025年09月'].append(post)
            
            # 生成归档内容
            result = []
            
            for month in sorted(date_groups.keys(), reverse=True):
                month_posts = date_groups[month]
                result.append(f"## 🗓️ {month}")
                result.append("")
                
                # 按分类分组
                category_groups = defaultdict(list)
                for post in month_posts:
                    category_groups[post['category']].append(post)
                
                # 按分类显示
                for category in sorted(category_groups.keys()):
                    display_name = category_display_names.get(category, category)
                    result.append(f"### {display_name}")
                    
                    for post in category_groups[category]:
                        result.append(f"- [{post['title']}]({post['path']}) - {post['date']}")
                    
                    result.append("")
            
            # 在最后添加统计信息
            result.append("---")
            result.append("")
            result.append("## 📊 统计信息")
            result.append("")
            result.append(f"- **总文章数**: {len(posts)}篇")
            result.append(f"- **分类数量**: {len(all_categories)}个")
            result.append("- **分类列表**: " + "、".join(sorted(all_categories)))
            
            return '\n'.join(result)
            
        except Exception as e:
            return f"## ❌ 生成错误\n\n生成归档时出错: {str(e)}\n\n请检查md文件格式或front matter语法。"
    
    @env.macro
    def auto_category():
        """
        Automatically generate category content from blog posts
        从md文件中完全自动获取分类信息，无硬编码
        """
        try:
            blog_posts_dir = Path("docs/blog/posts")
            if not blog_posts_dir.exists():
                return "## ❌ 错误\n\n无法找到博客文章目录\n\n"
            
            # 收集分类信息
            category_info = defaultdict(list)
            all_categories = set()
            
            # 遍历所有文章文件
            for md_file in blog_posts_dir.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    
                    # 提取front matter
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            front_matter_text = parts[1].strip()
                            try:
                                front_matter = yaml.safe_load(front_matter_text)
                                if not front_matter:
                                    continue
                                
                                title = front_matter.get('title', md_file.stem)
                                categories = front_matter.get('categories', [])
                                
                                # 处理分类
                                if isinstance(categories, list) and categories:
                                    for category in categories:
                                        cat_str = str(category)
                                        all_categories.add(cat_str)
                                        category_info[cat_str].append(title)
                                
                            except yaml.YAMLError:
                                continue
                
                except Exception:
                    continue
            
            if not category_info:
                return f"## 📝 调试信息\n\n找到 {len(all_categories)} 个分类，{len(category_info)} 个有文章的分类\n\n所有分类: {list(all_categories)}\n\n"
            
            # 生成分类页面内容  
            result = []
            result.append(f"## 🔍 找到{len(all_categories)}个分类")
            result.append("")
            
            # 编程语言部分
            result.append("## 🖥️ 编程语言")
            result.append("")
            
            for category in sorted(all_categories):
                cat_lower = category.lower()
                if cat_lower in ['cpp', 'python', 'csharp'] or 'c++' in cat_lower:
                    count = len(category_info[category])
                    
                    if cat_lower == 'cpp' or 'c++' in cat_lower:
                        display_name = 'C++'
                        icon = '🖥️'
                    elif cat_lower == 'python':
                        display_name = 'Python'
                        icon = '🐍'
                    else:
                        display_name = category
                        icon = '💻'
                    
                    result.append(f"### {icon} [{display_name}](category/{category}.html)")
                    result.append(f"- **文章数量**: {count}篇")
                    result.append(f"- **最新文章**: {', '.join(category_info[category][:3])}")
                    result.append("")
            
            # 开发框架和工具部分
            result.append("## 🔧 开发框架与工具")
            result.append("")
            
            for category in sorted(all_categories):
                cat_lower = category.lower()
                if 'autocad' in cat_lower or 'cad' in cat_lower or '工具' in cat_lower:
                    count = len(category_info[category])
                    result.append(f"### 🔧 [{category}](category/{category}.html)")
                    result.append(f"- **文章数量**: {count}篇")
                    result.append(f"- **最新文章**: {', '.join(category_info[category][:3])}")
                    result.append("")
            
            # 统计信息
            result.append("---")
            result.append("")
            result.append("## 📊 分类统计")
            result.append("")
            total_articles = sum(len(articles) for articles in category_info.values())
            result.append(f"- **总分类数**: {len(all_categories)}个")
            result.append(f"- **总文章数**: {total_articles}篇")
            
            return '\n'.join(result)
            
        except Exception as e:
            return f"## ❌ 生成错误\n\n{str(e)}\n\n"
```



## 发布到github中

### 使用GitHub Actions[¶](https://mkdoc-material.llango.com/publishing-your-site/#github-actions)

使用[GitHub Actions](https://github.com/features/actions)可以自动部署网站。在库的根目录下新建一个GitHub Actions workflow，比如：`.github/workflows/ci.yml`，并粘贴入以下内容：

Material for MkDocs

```
name: ci
on:
  push:
    branches:
      - master
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.x
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

此时，当一个新的提交推送到`master`或`main`时，我们的静态网站的内容将自动生成并完成部署。可以尝试推送一个提交来查看GitHub Actions的工作状况。

添加相关权限：

![image-20250919104024286](http://image.jerryma.xyz//images/20250919-image-20250919104024286.png)

![image-20250919104720037](http://image.jerryma.xyz//images/20250919-image-20250919104720037.png)

```

```