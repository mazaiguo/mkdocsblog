---
title: "increase the buffer of the AutoCAD text window"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - API
  - AutoCAD
  - AutoLISP
  - Unicode
description: "To begin with, I’d recommend the other post on Kean’s blog"
author: Autodesk
---
# increase the buffer of the AutoCAD text window

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/increase-the-buffer-of-the-autocad-text-window.html

## 文章内容

By Xiaodong Liang
To begin with, I’d recommend the other post on Kean’s blog
Increasing the size of AutoCAD’s command line history
you will know how to increase the size of command line history manually. At API side, there are two ways to access the Text Window buffer size, expressed in numbers of history lines: the
CmdHistLines environment variable, and the AutoCAD.AcadPreferencesDisplay.HistoryLines Automation property.
Here is how to set the environment variable from AutoLISP:
(setenv "CmdHistLines" "2048")
Here is how to set the Automation property from AutoLISP:
(vl-load-com)
(vla-put-historylines (vla-get-display (vla-get-preferences
(vlax-get-acad-object))) 2048)
Note: The value has to be between 25 and 2048.

## 评论

**内容**: Jürgen A. Becker said...
Hi,
this doesnt work for me.
Its has no effect.
Regards Jürgen
Reply
03/15/2013 at 11:06 AM

---
