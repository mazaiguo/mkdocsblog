---
title: Marp制作PPT
date: 2025-10-23
categories:
  - MarkDown
  - PPT
tags:
  - MarkDown
description: Marp 制作 PPT相关方案
author: JerryMa
---

# Marp制作PPT

## 打开vscode，下载Marp for VS Code

## 将Markdown Preview Enhanced禁用

## 编写自己的css文件

参考官方提供的demo(https://github.com/marp-team/awesome-marp)

???success  "custom.css"

    ```css
        /* 1. 基础全局样式（对应视觉风格类元素） */
        /* 色彩体系：商务风常用深蓝主色+灰色中性色，低饱和辅助色 */
        :root {
          --primary: #2e5a88; /* 主色：商务蓝，用于标题、重点 */
          --secondary: #8faadc; /* 辅助色：浅蓝，用于图标、装饰 */
          --neutral-dark: #333333; /* 中性深色：正文文字 */
          --neutral-light: #f5f7fa; /* 中性浅色：页面背景 */
          --border: #d0d9e2; /* 边框色：分隔线、模块边框 */
          --font-title: "Microsoft YaHei Bold", "Noto Sans SC Bold", sans-serif; /* 标题字体 */
          --font-body: "Microsoft YaHei", "Noto Sans SC", sans-serif; /* 正文字体 */
        }
        /* 图片尺寸预设类（商务场景常用） */
        .img-small {
          width: 30%;
        } /* 小图：适合图标、Logo组合 */
        .img-medium {
          width: 50%;
        } /* 中图：适合图文混排 */
        .img-large {
          width: 80%;
        } /* 大图：适合全屏展示细节 */
        .img-full {
          width: 100%;
        } /* 满屏图：适合封面、全屏截图 */
        /* 页面基础样式：统一背景、边距、字体 */
        section {
          background: var(--neutral-light);
          padding: 2.5rem; /* 页面内边距，避免内容贴边 */
          font-family: var(--font-body);
          color: var(--neutral-dark);
          line-height: 1.6; /* 行高优化可读性 */
        }
    
        /* 2. 标题样式（对应字体体系元素） */
        /* 封面页主标题 */
        h1 {
          font-family: var(--font-title);
          color: var(--primary);
          font-size: 2.5rem; /* 约36pt，符合清单要求 */
          margin-top: 4rem;
          margin-bottom: 1rem;
          text-align: center;
        }
    
        /* 内容页/目录页标题 */
        h2 {
          font-family: var(--font-title);
          color: var(--primary);
          font-size: 1.8rem; /* 约26pt，低于主标题 */
          margin-top: 0;
          margin-bottom: 1.5rem;
          padding-bottom: 0.5rem;
          border-bottom: 2px solid var(--secondary); /* 标题下加线，强化区分 */
        }
    
        /* 小标题/列表标题 */
        h3 {
          font-family: var(--font-title);
          color: var(--neutral-dark);
          font-size: 1.3rem; /* 约18pt */
          margin-top: 1rem;
          margin-bottom: 0.5rem;
        }
    
        /* 3. 文本与列表样式（对应内容模块类元素） */
        /* 正文文字 */
        p {
          font-size: 1rem; /* 约14pt，符合清单要求 */
          margin: 0.8rem 0;
        }
    
        /* 列表样式：统一项目符号，用主色点缀 */
        ul,
        ol {
          margin: 1rem 0 1rem 1.5rem;
          padding: 0;
        }
    
        ul li {
          list-style-type: square;
          list-style-color: var(--primary);
          margin: 0.5rem 0;
        }
    
        ol li {
          list-style-type: decimal;
          margin: 0.5rem 0;
        }
    
        /* 引用模块样式：灰色背景+左边界，突出引用内容 */
        blockquote {
          background: rgba(143, 173, 220, 0.1); /* 辅助色透明背景 */
          border-left: 4px solid var(--secondary);
          padding: 1rem 1.2rem;
          margin: 1rem 0;
          font-style: italic;
        }
    
        /* 4. 数据与图文模块样式（对应内容模块类元素） */
        /* 表格样式：商务风简洁表格，hover高亮 */
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 1.5rem 0;
          font-size: 0.9rem;
        }
    
        table th,
        table td {
          border: 1px solid var(--border);
          padding: 0.8rem 1rem;
          text-align: left;
        }
    
        table th {
          background: var(--primary);
          color: white;
          font-family: var(--font-title);
        }
    
        table tr:hover {
          background: rgba(143, 173, 220, 0.05);
        }
    
        /* 图片样式：统一图文排版，加轻微阴影 */
        img {
          max-width: 80%; /* 图片不超过页面宽度，避免溢出 */
          display: block;
          margin: 1.5rem auto; /* 图片居中 */
          border: 1px solid var(--border);
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 轻微阴影提升质感 */
        }
    
        /* 5. 辅助与装饰元素（对应交互与辅助类元素） */
        /* 分隔线：用于过渡页、模块分隔 */
        hr {
          border: none;
          border-top: 2px dashed var(--secondary);
          margin: 2rem 0;
        }
    
        /* 页码样式：固定在底部居中，商务风低调呈现 */
        .marp-bottom {
          font-size: 0.8rem;
          color: var(--neutral-dark);
          opacity: 0.7;
          text-align: center;
          padding-top: 1rem;
          border-top: 1px solid var(--border);
        }
    
        /* 封面页副标题样式：灰色，低于主标题层级 */
        .cover-subtitle {
          font-size: 1.2rem;
          color: var(--neutral-dark);
          opacity: 0.8;
          text-align: center;
          margin-bottom: 3rem;
        }
    
        /* 结尾页联系方式样式：右对齐，加图标占位 */
        .contact {
          text-align: right;
          margin-top: 3rem;
          font-size: 0.9rem;
        }
    
        .contact span {
          color: var(--primary);
          font-weight: bold;
        }
    
        /* 6. 数据对比模块（商务数据横向/纵向对比专用） */
        .data-comparison {
          display: grid;
          grid-template-columns: repeat(
            auto-fit,
            minmax(200px, 1fr)
          ); /* 自动适配列数 */
          gap: 1.5rem; /* 列间距 */
          margin: 2rem 0;
        }
    
        .data-item {
          background: white;
          border-radius: 4px;
          padding: 1.2rem;
          text-align: center;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); /* 轻微阴影突出模块 */
          border-top: 3px solid var(--primary); /* 顶部主色条强化识别 */
        }
    
        .data-item .label {
          font-size: 0.9rem;
          color: var(--neutral-dark);
          opacity: 0.8;
          margin-bottom: 0.5rem;
        }
    
        .data-item .value {
          font-family: var(--font-title);
          font-size: 1.8rem;
          color: var(--primary);
          margin: 0.3rem 0;
        }
    
        .data-item .change {
          font-size: 0.8rem;
          padding: 0.2rem 0.5rem;
          border-radius: 3px;
          display: inline-block;
        }
    
        .data-item .increase {
          background: rgba(76, 175, 80, 0.1); /* 增长用浅绿 */
          color: #4caf50;
        }
    
        .data-item .decrease {
          background: rgba(244, 67, 54, 0.1); /* 下降用浅红 */
          color: #f44336;
        }
    
        /* 7. 客户案例展示模块（含Logo+描述+评价） */
        .case-showcase {
          display: grid;
          grid-template-columns: repeat(
            auto-fit,
            minmax(280px, 1fr)
          ); /* 案例卡片自适应 */
          gap: 2rem;
          margin: 2rem 0;
        }
    
        .case-card {
          background: white;
          border-radius: 6px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
          border-left: 3px solid var(--secondary); /* 左侧辅助色条 */
        }
    
        .case-card .client-logo {
          width: 80px;
          height: 80px;
          margin: 0 auto 1rem; /* Logo居中 */
          border-radius: 50%; /* 圆形Logo容器 */
          background: var(--neutral-light);
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
        }
    
        .case-card .client-logo img {
          max-width: 60px;
          max-height: 60px;
          margin: 0; /* 覆盖全局img样式 */
          border: none;
          box-shadow: none;
        }
    
        .case-card .client-name {
          font-family: var(--font-title);
          text-align: center;
          margin-bottom: 0.8rem;
          color: var(--primary);
        }
    
        .case-card .case-desc {
          font-size: 0.9rem;
          color: var(--neutral-dark);
          line-height: 1.5;
          margin-bottom: 1rem;
        }
    
        .case-card .case-quote {
          font-size: 0.85rem;
          color: #666;
          font-style: italic;
          padding-left: 1rem;
          border-left: 2px solid var(--border);
        }
    
        /* 8. 多行多列通用布局（适配各类内容分栏） */
        /* 2列布局 */
        .two-columns {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.5rem;
          margin: 1.5rem 0;
        }
    
        /* 3列布局 */
        .three-columns {
          display: grid;
          grid-template-columns: 1fr 1fr 1fr;
          gap: 1rem;
          margin: 1.5rem 0;
        }
    
        /* 列内元素样式统一 */
        .column {
          padding: 1rem;
          background: white;
          border-radius: 4px;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
    
        .column h3 {
          margin-top: 0;
          color: var(--primary);
          font-size: 1.1rem;
        }
    
        .column p {
          font-size: 0.9rem;
        }
    
        /* 9. 核心图文布局样式（商务场景高频使用） */
        /* 基础图文容器：控制间距与对齐 */
        .image-text-container {
          display: grid;
          grid-template-columns: 1fr 1fr; /* 图文各占50%宽度 */
          gap: 2rem; /* 图文间距，避免拥挤 */
          align-items: center; /* 图文垂直居中对齐 */
          margin: 2rem 0;
        }
    
        /* 左图右文布局 */
        .image-left-text-right {
          grid-template-areas: "img text";
        }
    
        .image-left-text-right .img-box {
          grid-area: img;
        }
    
        .image-left-text-right .text-box {
          grid-area: text;
        }
    
        /* 右图左文布局 */
        .image-right-text-left {
          grid-template-areas: "text img";
        }
    
        .image-right-text-left .img-box {
          grid-area: img;
        }
    
        .image-right-text-left .text-box {
          grid-area: text;
        }
    
        /* 图文模块内图片样式：适配布局，强化商务质感 */
        .img-box img {
          width: 100%; /* 图片填满容器，不溢出 */
          max-width: 100%; /* 覆盖全局img样式 */
          height: auto; /* 保持图片比例 */
          border-radius: 6px; /* 轻微圆角，避免生硬 */
          box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1); /* 适度阴影，提升层次感 */
          border: 1px solid var(--border);
          margin: 0; /* 清除全局图片margin，避免错位 */
        }
    
        /* 图文模块内文字样式：优化层级与间距 */
        .text-box h3 {
          color: var(--primary);
          font-size: 1.4rem;
          margin-top: 0;
          margin-bottom: 1rem;
        }
    
        .text-box p {
          font-size: 0.95rem;
          line-height: 1.7;
          margin-bottom: 1rem;
        }
    
        /* 图文模块内重点文字：突出关键信息 */
        .text-box .highlight {
          color: var(--primary);
          font-weight: bold;
          border-bottom: 1px dotted var(--secondary); /* 下加点线，引导注意力 */
        }
    
        /* 10. 图片细节优化（适配不同商务场景） */
        /* 产品截图/方案示意图样式：带边框与说明区 */
        .product-screenshot {
          position: relative;
          margin: 2rem auto;
          max-width: 90%;
        }
    
        .product-screenshot img {
          border: 1px solid var(--border);
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        }
    
        /* 图片下方说明文字 */
        .product-screenshot .caption {
          text-align: center;
          font-size: 0.85rem;
          color: var(--neutral-dark);
          opacity: 0.8;
          margin-top: 0.8rem;
        }
    
        /* 图标+文字组合：用于要点说明 */
        .icon-text-group {
          display: flex;
          align-items: flex-start;
          gap: 0.8rem;
          margin-bottom: 1.2rem;
        }
    
        .icon-text-group .icon {
          width: 24px;
          height: 24px;
          margin-top: 0.3rem;
          color: var(--primary); /* 图标颜色与主色统一 */
        }
    
        .icon-text-group .text {
          flex: 1; /* 文字占满剩余空间 */
        }
    
        /* 11. 文字细节优化（提升可读性与专业性） */
        /* 数据/指标专用文字：突出数字 */
        .data-text {
          font-family: var(--font-title);
          color: var(--primary);
          font-size: 1.1rem;
        }
    
        /* 备注文字：弱化次要信息 */
        .note-text {
          font-size: 0.8rem;
          color: var(--neutral-dark);
          opacity: 0.7;
          margin-top: 0.5rem;
          font-style: italic;
        }
    
        /* 行动指引文字：引导下一步操作 */
        .cta-text {
          display: inline-block;
          padding: 0.5rem 1rem;
          background: rgba(46, 90, 136, 0.1); /* 主色透明背景 */
          color: var(--primary);
          font-weight: bold;
          border-radius: 4px;
          margin-top: 1rem;
        }
    
        /* 12. 引用与链接样式 */
        /* 强化引用盒子：商务场景突出重要观点 */
        .quote-box {
          background: white;
          border-radius: 6px;
          padding: 1.5rem;
          margin: 1.5rem 0;
          border-left: 4px solid var(--primary); /* 主色左边界，强化权威感 */
          box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
    
        .quote-box p {
          font-size: 1rem;
          color: #555;
          font-style: italic;
          margin: 0;
        }
    
        .quote-box .source {
          display: block;
          text-align: right;
          margin-top: 1rem;
          font-size: 0.85rem;
          color: var(--primary);
          font-weight: bold;
          font-style: normal;
        }
    
        /* 链接样式：商务风低调突出 */
        a {
          color: var(--primary);
          text-decoration: none;
          border-bottom: 1px solid var(--secondary); /* 下划线用辅助色 */
          padding-bottom: 0.1rem;
          transition: all 0.2s;
        }
    
        a:hover {
          color: #1A3D6C; /* 深色hover效果 */
          border-bottom-color: var(--primary);
        }
    
        /* 13. 多样化列表样式 */
        /* 圆形符号列表（默认列表增强） */
        ul.circle {
          list-style-type: circle;
          list-style-color: var(--secondary);
        }
    
        /* 方形符号列表 */
        ul.square {
          list-style-type: square;
          list-style-color: var(--primary);
        }
    
        /* 字母有序列表（A/B/C...） */
        ol.alpha {
          list-style-type: upper-alpha; /* 大写字母 */
        }
    
        /* 罗马数字列表（I/II/III...） */
        ol.roman {
          list-style-type: upper-roman; /* 大写罗马数字 */
        }
    
        /* 带图标的自定义列表（商务要点专用） */
        .custom-list {
          margin: 1.5rem 0;
          padding: 0;
        }
    
        .custom-list li {
          display: flex;
          align-items: flex-start;
          gap: 0.8rem;
          margin: 1rem 0;
          list-style: none;
        }
    
        .custom-list li::before {
          content: "•"; /* 自定义符号（可替换为图标） */
          color: var(--primary);
          font-size: 1.5rem;
          line-height: 0.8; /* 符号垂直居中 */
        }
    
        /* 14. 目录页样式（3种商务风设计） */
        /* 目录页通用基础 */
        .contents-page {
          padding: 3rem 4rem;
        }
    
        .contents-page h2 {
          text-align: center;
          margin-bottom: 2.5rem;
          border-bottom: none;
        }
    
        /* 样式1：简约编号目录（适合5-7项内容） */
        .contents-simple {
          max-width: 80%;
          margin: 0 auto;
        }
    
        .contents-simple li {
          font-size: 1.2rem;
          margin: 1.2rem 0;
          padding-left: 0.5rem;
          border-left: 3px solid transparent;
          transition: border-color 0.2s;
        }
    
        .contents-simple li:hover {
          border-left-color: var(--secondary);
        }
    
        .contents-simple li a {
          color: var(--neutral-dark);
          border-bottom: none;
        }
    
        /* 样式2：卡片式目录（适合3-5项重点内容） */
        .contents-cards {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1.5rem;
          margin-top: 2rem;
        }
    
        .contents-card {
          background: white;
          border-radius: 6px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.06);
          border-top: 3px solid var(--primary);
        }
    
        .contents-card .num {
          display: inline-block;
          width: 30px;
          height: 30px;
          background: var(--primary);
          color: white;
          border-radius: 50%;
          text-align: center;
          line-height: 30px;
          margin-right: 0.5rem;
          font-size: 0.9rem;
        }
    
        .contents-card a {
          color: var(--neutral-dark);
          text-decoration: none;
          border: none;
          font-weight: 500;
        }
    
        /* 样式3：进度条目录（适合分阶段内容） */
        .contents-progress {
          max-width: 90%;
          margin: 0 auto;
        }
    
        .contents-progress li {
          position: relative;
          padding: 1rem 0 1rem 4rem;
          margin: 1.5rem 0;
          border-bottom: 1px dashed var(--border);
        }
    
        .contents-progress li::before {
          content: attr(data-step); /* 从data-step获取序号 */
          position: absolute;
          left: 0;
          top: 0.8rem;
          width: 30px;
          height: 30px;
          background: var(--neutral-light);
          border: 2px solid var(--primary);
          color: var(--primary);
          border-radius: 50%;
          text-align: center;
          line-height: 28px;
          font-weight: bold;
        }
    
        /* 15. 封面页样式（2种商务风设计） */
        /* 样式1：简约品牌封面 */
        .cover-simple {
          background: linear-gradient(135deg, var(--neutral-light) 0%, #EEF2F7 100%);
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          text-align: center;
          padding: 2rem;
          height: 80%;
        }
    
        .cover-simple .title {
          font-size: 3rem;
          color: var(--primary);
          margin: 2rem 0 1rem;
          line-height: 1.3;
        }
    
        .cover-simple .subtitle {
          font-size: 1.3rem;
          color: #555;
          margin-bottom: 3rem;
        }
    
        .cover-simple .brand {
          margin-top: auto;
          display: flex;
          align-items: center;
          gap: 1rem;
        }
    
        .cover-simple .brand-logo {
          width: 60px;
          height: 60px;
        }
    
        .cover-simple .date {
          margin-top: 1rem;
          font-size: 0.9rem;
          color: #777;
        }
    
        /* 样式2：商务科技感封面 */
        .cover-tech {
          background: var(--primary);
          color: white;
          position: relative;
          overflow: hidden;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          text-align: center;
          padding: 2rem;
        }
    
        .cover-tech::after {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-image: radial-gradient(rgba(255,255,255,0.1) 1px, transparent 1px);
          background-size: 30px 30px;
          opacity: 0.5;
        }
    
        .cover-tech .title {
          font-size: 3.2rem;
          margin: 2rem 0 1rem;
          line-height: 1.3;
          position: relative; /* 覆盖背景网格 */
          color: white;
        }
    
        .cover-tech .subtitle {
          font-size: 1.2rem;
          opacity: 0.9;
          margin-bottom: 3rem;
          position: relative;
        }
    
        .cover-tech .footer {
          margin-top: auto;
          font-size: 0.9rem;
          opacity: 0.8;
          position: relative;
        }
    
        /* 封面页3：复古商务风 */
        .cover-vintage {
          background: #F8F5F0;
          display: flex;
          flex-direction: column;
          padding: 3rem 5rem;
          position: relative;
        }
    
        .cover-vintage::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 80px;
          background: var(--primary);
        }
    
        .cover-vintage .brand-badge {
          width: 120px;
          height: 120px;
          border-radius: 50%;
          background: white;
          border: 4px solid #E0D8C8;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 2rem;
          position: relative;
          z-index: 1;
        }
    
        .cover-vintage .brand-badge img {
          width: 80px;
          height: 80px;
          margin: 0;
          border: none;
          box-shadow: none;
        }
    
        .cover-vintage .title {
          font-family: "Noto Serif SC", serif; /* 衬线字体增强复古感 */
          font-size: 2.8rem;
          color: #3A3A3A;
          text-align: center;
          margin-bottom: 1rem;
          line-height: 1.4;
        }
    
        .cover-vintage .subtitle {
          font-size: 1.1rem;
          color: #666;
          text-align: center;
          margin-bottom: 4rem;
        }
    
        .cover-vintage .footer-info {
          display: flex;
          justify-content: space-between;
          font-size: 0.9rem;
          color: #777;
          border-top: 1px solid #E0D8C8;
          padding-top: 1rem;
          margin-top: auto;
        }
    
        /* 封面页4：极简数据风 */
        .cover-data {
          background: #FFFFFF;
          display: flex;
          flex-direction: column;
          padding: 4rem 3rem;
          position: relative;
        }
    
        .cover-data .data-points {
          position: absolute;
          top: 2rem;
          right: 2rem;
          display: flex;
          gap: 1.5rem;
        }
    
        .cover-data .data-item {
          text-align: right;
        }
    
        .cover-data .data-value {
          font-size: 1.8rem;
          color: var(--primary);
          font-weight: bold;
        }
    
        .cover-data .data-label {
          font-size: 0.8rem;
          color: #999;
        }
    
        .cover-data .title {
          font-size: 3rem;
          color: #222;
          margin: 6rem 0 1rem 0;
          line-height: 1.2;
        }
    
        .cover-data .subtitle {
          font-size: 1.2rem;
          color: #666;
          margin-bottom: 3rem;
        }
    
        .cover-data .product-tag {
          display: inline-block;
          padding: 0.4rem 1rem;
          background: var(--primary);
          color: white;
          border-radius: 20px;
          font-size: 0.9rem;
          margin-right: 0.8rem;
        }
    
        /* 目录页4：分栏对比目录 */
        .contents-compare {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
          padding: 3rem 4rem;
        }
    
        .contents-compare .column-title {
          font-size: 1.6rem;
          color: var(--primary);
          margin-bottom: 1.5rem;
          padding-bottom: 0.5rem;
          border-bottom: 2px solid var(--secondary);
        }
    
        .contents-compare .compare-list {
          margin: 0;
          padding: 0;
        }
    
        .contents-compare .compare-list li {
          list-style: none;
          margin: 1.2rem 0;
          font-size: 1.1rem;
          display: flex;
          align-items: center;
          gap: 0.8rem;
        }
    
        .contents-compare .compare-list li::before {
          content: "";
          width: 12px;
          height: 12px;
          border-radius: 50%;
        }
    
        /* 左侧列表标记色 */
        .contents-compare .left-list li::before {
          background: #F4A261;
        }
    
        /* 右侧列表标记色 */
        .contents-compare .right-list li::before {
          background: #2A9D8F;
        }
    
        /* 目录页5：图标引导目录 */
        .contents-icon {
          padding: 3rem 4rem;
        }
    
        .contents-icon h2 {
          text-align: center;
          margin-bottom: 3rem;
          border-bottom: none;
        }
    
        .contents-icon-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 2rem;
        }
    
        .contents-icon-item {
          background: white;
          border-radius: 8px;
          padding: 1.5rem;
          text-align: center;
          box-shadow: 0 3px 10px rgba(0,0,0,0.05);
          transition: transform 0.2s;
        }
    
        .contents-icon-item:hover {
          transform: translateY(-5px);
        }
    
        .contents-icon-item .icon {
          font-size: 2.5rem;
          color: var(--primary);
          margin-bottom: 1rem;
        }
    
        .contents-icon-item .item-title {
          font-size: 1.2rem;
          color: #333;
          margin-bottom: 0.5rem;
        }
    
        .contents-icon-item .item-desc {
          font-size: 0.85rem;
          color: #777;
        }
    ```



???sucess "example-custom.md"

    ```markdown
    ---
    marp: true
    style: |
      @import url('custom.css');
      /* 新增：补充页脚元素的强制不换行样式 */
      footer {
        display: flex !important; /* 弹性布局，让图片+文字横向排列 */
        align-items: center !important; /* 垂直居中对齐（解决图片与文字高度差） */
        justify-content: center !important; /* 整体水平居中 */
        white-space: nowrap !important; /* 强制不换行 */
        gap: 8px !important; /* 图片和文字之间留少量间距，避免拥挤 */
        bottom:21px;
      }
      /* 确保footer内图片不超宽，适配行高 */
      footer img {
        height: 20px !important; /* 与原配置h:20保持一致，避免图片过高导致换行 */
        width: auto !important;
        margin: 0 !important; /* 清除全局img的margin，防止错位 */
        border: none !important; /* 清除全局img的边框，避免样式干扰 */
        box-shadow: none !important; /* 清除全局img的阴影，保持简洁 */
      }
      paginate: true
      backgroundImage: url('https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_9_51_22_20251024-PixPin_2025-10-24_09-50-10.png')
      footer: "![h:24](https://statics.zwsoft.cn/web/global/img/header_logo.svg) 这是页脚"
    ---
    <!-- 封面页样式 -->
    <!-- 样式1：简约品牌封面 -->
    <section class="cover-simple">
      <h1 class="title">2024年度商务战略发布会</h1>
      <p class="subtitle">聚焦数字化转型，共话增长新机遇</p>
    
      <div class="brand">
        <img src="https://statics.zwsoft.cn/web/global/img/header_logo.svg" class="brand-logo" alt="品牌Logo">
        <span>某科技有限公司</span>
      </div>
      <p class="date">2024年10月24日 · 北京</p>
    </section>
    
    ---
    <!-- 样式2：商务科技感封面 -->
    <section class="cover-tech">
      <h1 class="title">智能数据分析平台<br>解决方案</h1>
      <p class="subtitle">驱动业务决策，释放数据价值</p>
    
      <div class="footer">
        某数据科技 ·  confidential
      </div>
    </section>


    ---
    <!-- 复古商务风封面（适合传统行业 / 年度汇报） -->
    <section class="cover-vintage">
      <div class="brand-badge">
        <img src="https://statics.zwsoft.cn/web/global/img/header_logo.svg" alt="企业Logo">
      </div>
      <h1 class="title">2024年度经营总结与规划</h1>
      <p class="subtitle">稳中求进 · 聚力增长</p>
      <div class="footer-info">
        <span>财务部 | 战略部 联合出品</span>
        <span>2024年12月</span>
      </div>
    </section>
    
    ---
    <!-- 极简数据风封面（适合科技 / 互联网产品） -->
    <section class="cover-data">
      <div class="data-points">
        <div class="data-item">
          <div class="data-value">98%</div>
          <div class="data-label">客户满意度</div>
        </div>
        <div class="data-item">
          <div class="data-value">500+</div>
          <div class="data-label">企业客户</div>
        </div>
      </div>
      <h1 class="title">DataMind<br>智能分析平台</h1>
      <p class="subtitle">让数据决策更简单</p>
      <div>
        <span class="product-tag">实时分析</span>
        <span class="product-tag">AI辅助</span>
        <span class="product-tag">多端适配</span>
      </div>
    </section>
    
    ---
    <!-- 分栏对比目录（适合 “现状 - 目标”“问题 - 方案” 类结构） -->
    <section>
      <h2 style="text-align: center; margin-bottom: 2rem;">项目规划：现状分析与目标设定</h2>
      <div class="contents-compare">
        <div class="left-column">
          <h3 class="column-title">当前现状</h3>
          <ul class="compare-list left-list">
            <li>系统响应延迟平均1.5s</li>
            <li>数据存储分散，无统一管理</li>
            <li>人工报表生成耗时2小时/份</li>
            <li>用户反馈问题响应超24小时</li>
          </ul>
        </div>
        <div class="right-column">
          <h3 class="column-title">优化目标</h3>
          <ul class="compare-list right-list">
            <li>系统响应延迟降至0.5s内</li>
            <li>建立统一数据中台</li>
            <li>报表自动化生成，耗时<5分钟</li>
            <li>用户问题响应≤4小时</li>
          </ul>
        </div>
      </div>
    </section>
    
    ---
    <!-- 图标引导目录（适合功能 / 模块展示，增强视觉识别） -->
    <section class="contents-icon">
      <h2>产品核心功能模块</h2>
      <div class="contents-icon-grid">
        <div class="contents-icon-item">
          <div class="icon">📊</div>
          <h3 class="item-title">数据可视化</h3>
          <p class="item-desc">12种图表类型，支持自定义配置</p>
        </div>
        <div class="contents-icon-item">
          <div class="icon">🔍</div>
          <h3 class="item-title">智能检索</h3>
          <p class="item-desc">自然语言查询，秒级定位数据</p>
        </div>
        <div class="contents-icon-item">
          <div class="icon">🔒</div>
          <h3 class="item-title">权限管理</h3>
          <p class="item-desc">多角色权限控制，数据安全隔离</p>
        </div>
        <div class="contents-icon-item">
          <div class="icon">📤</div>
          <h3 class="item-title">报表导出</h3>
          <p class="item-desc">支持PDF/Excel/PPT多种格式</p>
        </div>
      </div>
    </section>
    
    ---
    
    <!-- 样式2：卡片式目录 -->
    <section class="contents-page">
      <h2>产品方案大纲</h2>
      <div class="contents-cards">
        <div class="contents-card">
          <span class="num">1</span>
          <a href="#feature">核心功能介绍</a>
        </div>
        <div class="contents-card">
          <span class="num">2</span>
          <a href="#case">客户案例分析</a>
        </div>
        <div class="contents-card">
          <span class="num">3</span>
          <a href="#price">定价与服务</a>
        </div>
      </div>
    </section>
    
    ---
    
    <!-- 样式3：进度条目录 -->
    <section class="contents-page">
      <h2>项目实施计划</h2>
      <ul class="contents-progress">
        <li data-step="1">需求确认与方案设计 <small>（第1-2周）</small></li>
        <li data-step="2">系统开发与单元测试 <small>（第3-6周）</small></li>
        <li data-step="3">集成测试与用户验收 <small>（第7-8周）</small></li>
        <li data-step="4">上线部署与运维支持 <small>（第9周起）</small></li>
      </ul>
    </section>
    
    ---
    
    # 多样化列表
    ## 项目阶段
    <!-- 方形符号列表 -->
    <ul class="square">
      <li>需求调研（已完成）</li>
      <li>方案设计（进行中）</li>
      <li>开发测试（未开始）</li>
    </ul>
    
    ---
    
    ## 优先级排序
    <!-- 字母有序列表 -->
    <ol class="alpha">
      <li>核心功能开发</li>
      <li>数据接口对接</li>
      <li>用户手册编写</li>
    </ol>
    
    ---
    
    ## 核心优势
    <!-- 自定义图标列表 -->
    <ul class="custom-list">
      <li>7×24小时技术支持</li>
      <li>模块化部署，灵活扩展</li>
      <li>符合国家信息安全标准</li>
    </ul>
    
    ---
    <!-- # 目录页样式 -->
    <!-- 样式1：简约编号目录 -->
    <section class="contents-page">
      <h2>会议议程</h2>
      <ul class="contents-simple">
        <li>1. 开场致辞 <small>（10:00-10:10）</small></li>
        <li>2. 年度业绩回顾 <small>（10:10-10:40）</small></li>
        <li>3. 市场策略解读 <small>（10:40-11:20）</small></li>
        <li>4. 互动问答 <small>（11:20-11:40）</small></li>
      </ul>
    </section>





    ---
    
    <!-- 数据对比模块示例 -->
    ## 季度业绩对比
    <div class="data-comparison">
      <div class="data-item">
        <div class="label">Q1 销售额</div>
        <div class="value">¥248万</div>
        <div class="change increase">↑12.3%</div>
      </div>
      <div class="data-item">
        <div class="label">Q2 销售额</div>
        <div class="value">¥286万</div>
        <div class="change increase">↑15.3%</div>
      </div>
      <div class="data-item">
        <div class="label">Q3 销售额</div>
        <div class="value">¥265万</div>
        <div class="change decrease">↓7.3%</div>
      </div>
    </div>
    
    ---
    
    <!-- 客户案例展示示例 -->
    ## 客户成功案例
    <div class="case-showcase">
      <div class="case-card">
        <div class="client-logo">
          <img src="client1-logo.png" alt="客户Logo">
        </div>
        <h3 class="client-name">某科技有限公司</h3>
        <p class="case-desc">通过我们的解决方案，客户运营效率提升40%，成本降低25%。</p>
        <p class="case-quote">"合作后团队协作效率显著提升，系统稳定性超出预期。"</p>
      </div>
      <div class="case-card">
        <!-- 第二个案例卡片 -->
      </div>
    </div>
    
    ---
    <!-- 3列布局示例 -->
    ## 核心优势
    <div class="three-columns">
      <div class="column">
        <h3>高效部署</h3>
        <p>平均部署周期缩短至7天，支持多场景快速适配</p>
      </div>
      <div class="column">
        <h3>安全可靠</h3>
        <p>银行级加密技术，全年服务可用性99.9%</p>
      </div>
      <div class="column">
        <h3>定制服务</h3>
        <p>专属顾问团队，提供7×24小时一对一支持</p>
      </div>
    </div>
    
    ---
    
    <!-- 左图右文：产品介绍示例 -->
    ## 核心产品功能
    <div class="image-text-container image-left-text-right">
      <div class="img-box">
        <img src="https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_8_58_25_20251024-image-20251024085824015.png" alt="产品界面">
      </div>
      <div class="text-box">
        <h3>智能数据分析平台</h3>
        <p>平台支持<span class="highlight">实时数据接入</span>，可自动生成可视化报表，无需手动配置。</p>
        <p>核心优势：</p>
        <div class="icon-text-group">
          <div class="icon">📊</div>
          <div class="text">内置12种图表类型，满足不同分析场景</div>
        </div>
        <div class="icon-text-group">
          <div class="icon">⚡</div>
          <div class="text">数据处理速度提升<span class="data-text">60%</span>，支持百万级数据量</div>
        </div>
        <p class="note-text">注：需搭配企业级数据源使用</p>
      </div>
    </div>
    
    ---
    
    <!-- 右图左文：方案说明示例 -->
    ## 客户解决方案
    <div class="image-text-container image-right-text-left">
      <div class="text-box">
        <h3>全流程数字化改造</h3>
        <p>为某制造企业提供从生产到销售的<span class="highlight">全链路数字化方案</span>，解决信息孤岛问题。</p>
        <p>实施效果：</p>
        <ul>
          <li>生产效率提升 <span class="data-text">28%</span></li>
          <li>库存周转天数减少 <span class="data-text">15天</span></li>
          <li>客户响应时间缩短 <span class="data-text">50%</span></li>
        </ul>
        <span class="cta-text">查看完整案例 →</span>
      </div>
      <div class="img-box">
        <div class="product-screenshot">
          <img src="https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_8_58_25_20251024-image-20251024085824015.png" alt="方案流程图">
          <div class="caption">方案实施流程图（2024版）</div>
        </div>
      </div>
    </div>
    
    ---
    # 引用与链接
    ## 行业观点
    <blockquote class="quote-box">
      数字化转型不是选择题，而是生存题。企业需在数据中台建设上加大投入，才能在未来3年内保持竞争力。
      <span class="source">—— 某咨询公司《2024数字化报告》</span>
    </blockquote>
    
    查看完整报告：<a href="https://example.com/report">下载PDF版本</a>
    
    ```

![image-20251024103316945](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_10_33_18_20251024-image-20251024103316945.png)

![image-20251024103340595](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_10_33_41_20251024-image-20251024103340595.png)

![image-20251024103410801](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_10_34_11_20251024-image-20251024103410801.png)

![image-20251024103428017](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_10_34_29_20251024-image-20251024103428017.png)

![image-20251024103454896](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_10_34_56_20251024-image-20251024103454896.png)

![image-20251024103513205](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2025/10/24_10_35_14_20251024-image-20251024103513205.png)

1. **适配调整**：若需修改颜色、间距，可调整 CSS 中的var(--primary)（主色）、gap（间距）、font-size（字号）等参数。

1. **素材替换**：demo 中的logo.png product-tag等，需替换为实际品牌素材，图标可通过 Emoji 或 SVG 图标库替换（如 Font Awesome）。