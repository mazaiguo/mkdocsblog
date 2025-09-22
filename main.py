"""
MkDocs macros for auto-generating archive content
"""
import os
import re
import yaml
from pathlib import Path
from datetime import datetime, date  # 顶部导入
from collections import defaultdict
import urllib.parse

def generate_url_slug(title):
    """根据实际URL格式生成URL片段"""
    # 1. 转为小写
    slug = title.lower()
    
    # 2. 特殊处理：如果以点号开头，删除点号并在后面添加分隔符
    if slug.startswith('.'):
        slug = slug[1:]  # 删除开头的点号
        # 在英文和中文之间添加分隔符
        slug = re.sub(r'^([a-z]+)(?=[\u4e00-\u9fff])', r'\1-', slug)
    
    # 3. 处理其他点号 - 直接删除（保持原有行为）
    slug = slug.replace('.', '')
    
    # 4. 处理括号（删除括号，保留内容）
    slug = re.sub(r'[()（）]', '', slug)
    
    # 5. 处理连续的+号（C++等）
    slug = re.sub(r'\+{2,}', '', slug)
    
    # 6. 只对没有自然分隔符的长字符串添加中英文分隔符
    # 检查是否需要添加分隔符（没有空格或连字符的长字符串）
    # if ' ' not in slug and '-' not in slug and len(slug) > 10:
    #     # 在中英文交界处添加分隔符
    #     slug = re.sub(r'(?<=[a-z0-9])(?=[\u4e00-\u9fff])', '-', slug)
    #     slug = re.sub(r'(?<=[\u4e00-\u9fff])(?=[a-z0-9])', '-', slug)
    
    # 7. 将多个空格合并为一个，然后转为连字符
    slug = re.sub(r'\s+', '-', slug)
    
    # 8. 清理多余的连字符
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    
    # 9. URL编码
    return urllib.parse.quote(slug)

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
                                date_val = front_matter.get('date', '2025-09-18')
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
                                    'date': str(date_val),
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
                    category_display_names[category] = 'CPP开发'
                elif cat_lower == 'python' or 'python' in cat_lower:
                    category_display_names[category] = 'Python开发'
                elif 'autocad' in cat_lower or 'cad' in cat_lower:
                    category_display_names[category] = 'AutoCAD开发'
                elif cat_lower == 'csharp' or 'c#' in cat_lower or '.net' in cat_lower:
                    category_display_names[category] = 'C#/.NET开发'
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
            nBlogCount = 0
            # 遍历所有文章文件
            for md_file in blog_posts_dir.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    
                    nBlogCount += 1
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
                                date_val = front_matter.get('date', '2025-09-18')

                                # 处理分类
                                if isinstance(categories, list) and categories:
                                    for category in categories:
                                        cat_str = str(category).strip().lower()  # 归一化
                                        all_categories.add(cat_str)
                                        category_info[cat_str].append((title, date_val, md_file.stem))
                                
                            except yaml.YAMLError:
                                continue
                             
                except Exception:
                    continue
            
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
                        display_name = 'CPP'
                        icon = '🖥️'
                    elif cat_lower == 'python':
                        display_name = 'Python'
                        icon = '🐍'
                    else:
                        display_name = category
                        icon = '💻'
                    
                    # 添加分类标题
                    result.append(f"### {icon} [{display_name}](category/{cat_lower}.html)")
                    result.append(f"- **文章数量**: {count}篇")
                    
                    latest = []
                    print(f"category={category}, items={category_info[category]}")
                    for t, d, stem in sorted(category_info[category], key=lambda x: x[1], reverse=True)[:3]:
                        url = f"{generate_url_slug(t)}.html"  # 使用title转小写再编码
                        dt = None
                        try:
                            if isinstance(d, datetime):
                                dt = d
                            elif isinstance(d, date):
                                dt = datetime.combine(d, datetime.min.time())
                            elif isinstance(d, str) and len(d) == 10:
                                dt = datetime.strptime(d, "%Y-%m-%d")
                        except Exception as ex:
                            pass
                        if dt:
                            url = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/{generate_url_slug(t)}.html"
                        latest.append(f"[{t}]({url})")
                    result.append(f"- **最新文章**: {', '.join(latest)}")
                    result.append("")
                else:
                    icon = '💻'
                    result.append(f"### {icon} [{cat_lower}](category/{cat_lower}.html)")
                    result.append(f"- **文章数量**: {len(category_info[category])}篇")
                    # 修正这里，生成带链接的最新文章
                    latest = []
                    print(f"category={category}, items={category_info[category]}")
                    for t, d, stem in sorted(category_info[category], key=lambda x: x[1], reverse=True)[:3]:
                        url = f"{generate_url_slug(t)}.html"  # 使用title转小写再编码
                        dt = None
                        try:
                            if isinstance(d, datetime):
                                dt = d
                            elif isinstance(d, date):
                                dt = datetime.combine(d, datetime.min.time())
                            elif isinstance(d, str) and len(d) == 10:
                                dt = datetime.strptime(d, "%Y-%m-%d")
                        except Exception as ex:
                            pass
                        if dt:
                            url = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/{generate_url_slug(t)}.html"
                        latest.append(f"[{t}]({url})")
                    result.append(f"- **最新文章**: {', '.join(latest)}")
                    result.append("")
            
            # 开发框架和工具部分
            result.append("## 🔧 开发框架与工具")
            result.append("")
            
            for category in sorted(all_categories):
                cat_lower = category.lower()
                if 'autocad' in cat_lower or 'cad' in cat_lower or '工具' in cat_lower:
                    count = len(category_info[category])
                    
                    # 添加分类标题
                    if 'autocad' in cat_lower or 'cad' in cat_lower:
                        icon = '🏗️'
                        display_name = 'AutoCAD/CAD开发'
                    else:
                        icon = '🔧'
                        display_name = category
                    
                    result.append(f"### {icon} [{display_name}](category/{cat_lower}.html)")
                    result.append(f"- **文章数量**: {count}篇")
                    
                    latest = []
                    print(f"category={category}, items={category_info[category]}")
                    for t, d, stem in sorted(category_info[category], key=lambda x: x[1], reverse=True)[:3]:
                        url = f"{generate_url_slug(t)}.html"  # 使用title转小写再编码
                        dt = None
                        try:
                            if isinstance(d, datetime):
                                dt = d
                            elif isinstance(d, date):
                                dt = datetime.combine(d, datetime.min.time())
                            elif isinstance(d, str) and len(d) == 10:
                                dt = datetime.strptime(d, "%Y-%m-%d")
                        except Exception as ex:
                            pass
                        if dt:
                            url = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/{generate_url_slug(t)}.html"
                        latest.append(f"[{t}]({url})")
                    result.append(f"- **最新文章**: {', '.join(latest)}")
                    result.append("")
            
            # 统计信息
            result.append("---")
            result.append("")
            result.append("## 📊 分类统计")
            result.append("")
            total_articles = sum(len(articles) for articles in category_info.values())
            result.append(f"- **总分类数**: {len(all_categories)}个")
            result.append(f"- **总文章数**:  {nBlogCount}篇")
            
            return '\n'.join(result)
            
        except Exception as e:
            return f"## ❌ 生成错误\n\n{str(e)}\n\n"

    @env.macro
    def auto_tag():
        """
        Automatically generate tag content from blog posts
        从md文件中完全自动获取标签信息，无硬编码
        """

        try:
            all_tags = set()
            tag_info = defaultdict(list)
            blog_posts_dir = Path("docs/blog/posts")
            if not blog_posts_dir.exists():
                return "## ❌ 错误\n\n无法找到博客文章目录\n\n"
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

                                tags = front_matter.get('tags', [])

                                # 处理标签
                                if isinstance(tags, list) and tags:
                                    for tag in tags:
                                        tag_str = str(tag)
                                        all_tags.add(tag_str)
                                        tag_info[tag_str].append(md_file.stem)

                            except yaml.YAMLError:
                                continue

                except Exception:
                    continue

            if not tag_info:
                return f"## 📝 调试信息\n\n找到 {len(all_tags)} 个标签，{len(tag_info)} 个有文章的标签\n\n所有标签: {list(all_tags)}\n\n"

            # 生成标签页面内容
            result = []
            result.append(f"## 🔍 找到{len(all_tags)}个标签")
            result.append("")

            for tag in sorted(all_tags):
                count = len(tag_info[tag])
                result.append(f"### [{tag}](tag/{tag}.html)") # 修改为tag/{tag}.html
                result.append(f"- **文章数量**: {count}篇")
                result.append(f"- **最新文章**: {', '.join(tag_info[tag][:3])}")
                result.append("")   
            return '\n'.join(result)

        except Exception as e:
            return f"## ❌ 生成错误\n\n{str(e)}\n\n"

    @env.macro
    def auto_home_category():
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
            nBlogCount = 0
            # 遍历所有文章文件
            for md_file in blog_posts_dir.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    
                    nBlogCount += 1
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
                                date_val = front_matter.get('date', '2025-09-18')

                                # 处理分类
                                if isinstance(categories, list) and categories:
                                    for category in categories:
                                        cat_str = str(category).strip().lower()  # 归一化
                                        all_categories.add(cat_str)
                                        category_info[cat_str].append((title, date_val, md_file.stem))
                                
                            except yaml.YAMLError:
                                continue
                             
                except Exception:
                    continue
            
            # if not category_info:
            #     return f"## 📝 调试信息\n\n找到 {len(all_categories)} 个分类，{len(category_info)} 个有文章的分类\n\n所有分类: {list(all_categories)}\n\n"
            
            # 生成分类页面内容  
            result = []
            result.append(f"## 🔍 找到{len(all_categories)}个分类")
            result.append("")
            
            # 编程语言部分
            result.append("## 🖥️ 编程语言")
            result.append("")
            
            for category in sorted(all_categories):
                cat_lower = category.lower()
                if 'windows' in cat_lower or 'window' in cat_lower:
                    count = len(category_info[category])
                    
                    if cat_lower == 'window' or 'windows' in cat_lower:
                        display_name = 'windows程序'
                        icon = '🔨'
                    else:
                        display_name = category
                        icon = '💻'
                    
                    # 添加分类标题
                    result.append(f"### {icon} [{display_name}](blog/category/{cat_lower}.html)")
                    result.append(f"- **文章数量**: {count}篇")
                    
                    latest = []
                    print(f"category={category}, items={category_info[category]}")
                    for t, d, stem in sorted(category_info[category], key=lambda x: x[1], reverse=True)[:]:
                        url = f"blog/{generate_url_slug(t)}.html"  # 使用title转小写再编码
                        dt = None
                        try:
                            if isinstance(d, datetime):
                                dt = d
                            elif isinstance(d, date):
                                dt = datetime.combine(d, datetime.min.time())
                            elif isinstance(d, str) and len(d) == 10:
                                dt = datetime.strptime(d, "%Y-%m-%d")
                        except Exception as ex:
                            pass
                        if dt:
                            url = f"blog/{dt.year}/{dt.month:02d}/{dt.day:02d}/{generate_url_slug(t)}.html"
                        latest.append(f"<li>[{t}]({url})</li>")
                    result.append(f"- **最新文章**: {' '.join(latest)}")
                    result.append("")
                else:
                    icon = '🛠️'
                    result.append(f"### {icon} [{cat_lower}](blog/category/{cat_lower}.html)")
                    result.append(f"- **文章数量**: {len(category_info[category])}篇")
                    # 修正这里，生成带链接的最新文章
                    latest = []
                    print(f"category={category}, items={category_info[category]}")
                    for t, d, stem in sorted(category_info[category], key=lambda x: x[1], reverse=True)[:]:
                        url = f"blog/{generate_url_slug(t)}.html"  # 使用title转小写再编码
                        dt = None
                        try:
                            if isinstance(d, datetime):
                                dt = d
                            elif isinstance(d, date):
                                dt = datetime.combine(d, datetime.min.time())
                            elif isinstance(d, str) and len(d) == 10:
                                dt = datetime.strptime(d, "%Y-%m-%d")
                        except Exception as ex:
                            pass
                        if dt:
                            url = f"blog/{dt.year}/{dt.month:02d}/{dt.day:02d}/{generate_url_slug(t)}.html"
                        latest.append(f"<li>[{t}]({url})</li>")
                    result.append(f"- **最新文章**: {' '.join(latest)}")
                    result.append("")
            
            # 开发框架和工具部分
            result.append("## 🏗️ 开发框架与工具")
            result.append("")
            
            for category in sorted(all_categories):
                cat_lower = category.lower()
                if 'autocad' in cat_lower or 'cad' in cat_lower or '工具' in cat_lower:
                    count = len(category_info[category])
                    
                    # 添加分类标题
                    if 'autocad' in cat_lower or 'cad' in cat_lower:
                        icon = '🏗️'
                        display_name = 'AutoCAD/CAD开发'
                    else:
                        icon = '✏️'
                        display_name = category
                    
                    result.append(f"### {icon} [{display_name}](blog/category/{cat_lower}.html)")
                    result.append(f"- **文章数量**: {count}篇")
                    
                    latest = []
                    print(f"category={category}, items={category_info[category]}")
                    for t, d, stem in sorted(category_info[category], key=lambda x: x[1], reverse=True)[:]:
                        url = f"blog/{generate_url_slug(t)}.html"  # 使用title转小写再编码
                        dt = None
                        try:
                            if isinstance(d, datetime):
                                dt = d
                            elif isinstance(d, date):
                                dt = datetime.combine(d, datetime.min.time())
                            elif isinstance(d, str) and len(d) == 10:
                                dt = datetime.strptime(d, "%Y-%m-%d")
                        except Exception as ex:
                            pass
                        if dt:
                            url = f"blog/{dt.year}/{dt.month:02d}/{dt.day:02d}/{generate_url_slug(t)}.html"
                        latest.append(f"<li>[{t}]({url})</li>")
                    result.append(f"- **最新文章**: {''.join(latest)}")
                    result.append("")
            
            # 统计信息
            result.append("---")
            result.append("")
            result.append("## 📊 分类统计")
            result.append("")
            total_articles = sum(len(articles) for articles in category_info.values())
            result.append(f"- **总分类数**: {len(all_categories)}个")
            result.append(f"- **总文章数**:  {nBlogCount}篇")
            
            return '\n'.join(result)
            
        except Exception as e:
            return f"## ❌ 生成错误\n\n{str(e)}\n\n"
