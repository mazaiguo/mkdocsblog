---
title: Markdown 制作 PPT
date: 2025-10-23
categories:
  - MarkDown
  - PPT
tags:
  - MarkDown
description: Markdown 制作 PPT相关方案
author: JerryMa
---

用 **Markdown 制作 PPT** 的方式现在非常流行，因为它能让你用简洁的语法生成美观的幻灯片。以下是目前主流的几种工具（按技术类型和用途分类）：

------

## 🧭 一、基于 HTML/浏览器 的方案（最主流）

这些工具将 Markdown 转换为 HTML 幻灯片，可直接在浏览器中播放，也能导出 PDF。

### 1️⃣ **Marp / Marp CLI / Marp for VS Code**

- 🔧 **官网**：https://marp.app/

- 🧩 **特点**：

  - 支持标准 Markdown；
  - 主题丰富（如 `default`, `gaia`, `uncover`）；
  - 可以直接在 VS Code 中编写并实时预览；
  - 可导出为 **HTML、PDF、PPTX**。

- 💡 **用法示例**：

  ```bash
  ---
  theme: default
  class: lead
  paginate: true
  ---
  
  # 欢迎使用 Marp
  
  ---
  
  ## 第二页
  - 支持 Markdown 列表
  - 支持代码高亮
  ```

------

### 2️⃣ **reveal.js + markdown**

- 🔧 **官网**：https://revealjs.com/

- 📦 **安装**：

  ```bash
  npm install reveal-md -g
  ```

- 💡 **用法**：

  ```bash
  reveal-md slides.md
  ```

- 🌟 **优点**：

  - 动画、过渡效果非常强；
  - 可通过插件支持演讲者视图、代码高亮；
  - 可导出 PDF；
  - 可自定义主题与模板；

- 🚀 **适合人群**：技术演讲者、开发者、科研展示。

------

### 3️⃣ **Slidev（基于 Vue 3 的现代化方案）**

- 🔧 **官网**：https://sli.dev/

- ⚙️ **安装**：

  ```bash
  npm init slidev@latest
  npm run dev
  ```

- 💡 **特点**：

  - 支持 Markdown + Vue 组件；
  - 内置代码高亮、数学公式、绘图；
  - 热重载编辑；
  - 支持导出为 PDF、静态网站；
  - 视觉效果极佳。

- 📘 **用法**：

  ```bash
  ---
  theme: default
  ---
  
  # Hello Slidev
  
  You can use **Markdown**, and even Vue components!
  ```

------

### 4️⃣ **Deckset（Mac 专用）**

- 🔧 **官网**：https://www.deckset.com/
- 💻 **平台**：macOS
- 💡 **特点**：
  - 直接打开 Markdown 文件生成漂亮幻灯片；
  - 模板多、界面友好；
  - 适合非程序员；
- 💰 **收费**（约 $35）。

------

## 🧱 二、桌面软件方案

### 5️⃣ **Typora + Marp CLI**

- 在 Typora（Markdown 编辑器）中写好内容；

- 用 Marp CLI 导出为 PPT 或 PDF；

  ```bash
  marp myslides.md --pptx
  ```

------

## 🧠 三、在线工具

| 工具名              | 特点                                          | 地址                  |
| ------------------- | --------------------------------------------- | --------------------- |
| **HackMD / CodiMD** | 在线协作编辑 + Markdown 幻灯片模式            | https://hackmd.io/    |
| **Slides.com**      | 类似 PowerPoint 的在线编辑器，可导入 Markdown | https://slides.com/   |
| **GitPitch**        | 面向 GitHub 项目的在线 Markdown 幻灯片        | https://gitpitch.com/ |

------

## 🧩 四、科研类 / LaTeX 集成方案

### 6️⃣ **Pandoc + Beamer**

- 🔧 **命令行转换**：

  ```bash
  pandoc slides.md -t beamer -o slides.pdf
  ```

- 🎓 **适合学术汇报**；

- 支持数学公式、参考文献、LaTeX 样式。

------

## ✅ 推荐总结

| 需求                      | 推荐工具                      |
| ------------------------- | ----------------------------- |
| 想快速生成、导出 PDF/PPT  | 🟩 **Marp / Marp for VS Code** |
| 想要漂亮动画和在线演示    | 🟦 **reveal.js / reveal-md**   |
| 想要现代感 + Vue 扩展能力 | 🟪 **Slidev**                  |
| Mac 用户、追求简洁        | 🟨 **Deckset**                 |
| 学术报告、论文展示        | 🟥 **Pandoc + Beamer**         |