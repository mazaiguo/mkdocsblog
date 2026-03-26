---
title: "Insert a newline character in MText"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C#
  - C++
  - ObjectARX
  - Unicode
description: "For MText (.NET) or AcDbMText (ObjectARX C++) entities, the newline character is \P as opposed to the traditional '\n' escape character, so setting..."
author: Autodesk
---
# Insert a newline character in MText

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/insert-a-newline-character-in-mtext.html

## 文章内容

By Augusto Goncalves
For MText (.NET) or AcDbMText (ObjectARX C++) entities, the newline character is \P as opposed to the traditional '\n' escape character, so setting the content use \\P C#/C++ (double backslash is interpreted as one) or \P for VB.NET.
(C#)
MText myText = // open me here
myText.Contents = "First line \\P Second line";
(VB.NET)
Dim myText As MText = ' open me here
myText.Contents = "First line \P Second line"
For a complete list of multi-line text formatting characters, visit Format Codes for Alternate Text Editor Reference.

## 评论

**内容**: Maxence said...
You can use the MText.LineBreak constant, but this property returns \p (lowercase) and the code needs to be in upper case...
So :
myText.Contents = "First line" + MText.LineBreak.ToUpper() + "Second line";
Reply
08/17/2015 at 02:06 AM

---
