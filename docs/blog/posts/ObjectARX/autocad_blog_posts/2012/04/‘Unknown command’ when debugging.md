---
title: "‘Unknown command’ when debugging"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Plugin
description: "The most common reason why your command would not be recognized by AutoCAD when debugging your application is that the ‘Copy Local’ property of the..."
author: Autodesk
---
# ‘Unknown command’ when debugging

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/unknown-command-when-debugging.html

## 文章内容

By Adam Nagy
The most common reason why your command would not be recognized by AutoCAD when debugging your application is that the ‘Copy Local’ property of the reference to AcMgd.dll is not set to ‘False’ and so both the original AcMgd.dll from the AutoCAD folder, plus its copy from your project’s output folder will be loaded into AutoCAD.
Best to set the ‘Copy Local’ property of all references to AutoCAD API assemblies (AcMgd.dll, AcDbMgd.dll, etc) to ‘False’.
This important step is also mentioned in My First AutoCAD Plug-in >> Lesson 1 >> Step 7

## 评论

**内容**: Account Deleted said...
Adam!
There is also another reason why command would not be recognized: if command class is not public: http://forums.autodesk.com/t5/NET/AutoCad2010-with-Visualstudio-2008-c/td-p/3431991
Reply
04/27/2012 at 02:37 PM

---
**内容**: Adam Nagy said...
Hi Alexander,
Thanks for the comment. :)
Yes, that could be another issue. In this post I only focused on the one I found the most common.
Reply
04/30/2012 at 07:08 AM

---
**内容**: Ben said...
If anyone's reading this, you might also need to load your dll from a trusted location. if you want to add another location do so like this: autocad --> File ---> options ---> add the folder to the trusted location.
Reply
04/27/2017 at 06:40 PM

---
