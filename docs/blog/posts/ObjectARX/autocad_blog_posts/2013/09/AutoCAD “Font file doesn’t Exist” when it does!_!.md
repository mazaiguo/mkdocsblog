---
title: "AutoCAD “Font file doesn’t Exist” when it does!?!"
date: 2013-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "One of my developers was trying to create a toolbar button which automatically setup some text styles/parameters. Everything was fine except that o..."
author: Autodesk
---
# AutoCAD “Font file doesn’t Exist” when it does!?!

发布日期: 2013-09-01

原始链接: https://adndevblog.typepad.com/autocad/2013/09/autocad-font-file-doesnt-exist-when-it-does.html

## 文章内容

by Fenton Webb
One of my developers was trying to create a toolbar button which automatically setup some text styles/parameters. Everything was fine except that on some machines, the button would fail – the error was “Font file doesn’t exist”. He was using a very commonly used font file “arial.ttf”, indeed arial.ttf is the default font for the “Standard” AutoCAD style.
It seems there are very important updates the Font packs that you need to include (update) with your Windows installation – check out http://www.microsoft.com/typography/fonts/
I’m guessing Windows update also includes these Font updates as ‘Optional’ – best install them for an easy life!

## 评论

**内容**: Paul Mitchell said...
We have a simple lisp routine which creates a few text styles in AutoCAD 2014 (windows 7) A few people have the same issue while others don't. The lisp route errors out because the file does not exist, however, they can create the style via the dialog... Others are not having the issue. What's really going on? I've seen other posts regarding this issue but all responses are workarounds. We've updated the Arial.ttf font with no results. The dialog works while the command line doesn't.
Reply
08/19/2014 at 04:44 PM

---
