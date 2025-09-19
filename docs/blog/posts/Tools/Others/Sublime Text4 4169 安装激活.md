---
title: Sublime Text4 4169 安装激活
date: 2024-07-19
categories:
  - 开发工具
  - 软件安装
tags:
  - Sublime Text
  - 编辑器
  - 破解
  - 安装教程
description: Sublime Text4编辑器4169版本的详细安装和激活教程
author: JerryMa
---
# Sublime Text4 4169 安装激活

## 下载地址

https://download.sublimetext.com/sublime_text_build_4169_x64_setup.exe

## 激活

默认安装路径：C:\Program Files\Sublime Text

安装之后，使用sublime text 打开安装目录下的sublime_text.exe文件。

Ctrl + F 搜到到

```bash
80 7805 000f
94c1
```

更改为

```bash
c6 4005 0148
85c9
```

![](http://image.jerryma.xyz//images/20240719-20240719154806.png)

然后另存到其他路径，然后关闭sublime text，将原sublime_text.exe进行替换即可。

## 关闭更新

### 打开Sublime，在最上方菜单栏点击Preferences(中文“首选项”)，然后点击(中文“设置-特定语法”)

在花括号中输入以下语句：
"ignored_packages": [],
"update_check":false,
然后，Ctrl+S保存
注：切记是在英文模式下！！！

![image-20240719162525183](http://image.jerryma.xyz//images/20240719-image-20240719162525183.png)

### 打开Sublime，在最上方菜单栏点击Preferences(中文“首选项”)，然后点击Settings(中文“设置”)

在花括号中输入以下语句：
"update_check":false,
注：切记是在英文模式下！！！

![image-20240719162626571](http://image.jerryma.xyz//images/20240719-image-20240719162626571.png)

## ☞ How to install free evaluation for Sublime Text:

```bash
1. Package Control ‣ Install Package ‣ Theme - Monokai Pro
2. Command Palette ‣ Monokai Pro: select theme
```

## ConvertToUTF8

```bash
Package Control ‣ Install Package ‣ ConvertToUTF8
```

## BracketHighlighter

```bash
Package Control ‣ Install Package ‣ BracketHighlighter
```

## Chinese

```bash
Package Control ‣ Install Package ‣ Chinese
```

