---
title: "WPF Databinding to the CommandLine Colors"
date: 2013-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Using WPF databinding, you can actually bind your WPF colors to the CommandLine color settings."
author: Autodesk
---
# WPF Databinding to the CommandLine Colors

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/wpf-databinding-to-the-commandline-colors.html

## 文章内容

by Fenton Webb
Using WPF databinding, you can actually bind your WPF colors to the CommandLine color settings.
This can be achieved using the Autodesk.AutoCAD.Windows.Data.DataBindings.ColorSettings ObserveableCollection.
The possible color settings property names are:
CommandLineForeground
CommandLineBackground
CommandLineHistoryForeground
CommandLineHistoryBackground
CommandLineTempPromptForeground
CommandLineTempPromptBackground
CommandLineKeywordHighlight
CommandLineKeywordBackground
CommandLineKeywordHover
If you want a good example of how to use the Autodesk.AutoCAD.Windows.Data.DataBindings collections then check out this blog http://adndevblog.typepad.com/autocad/2012/03/using-autocad-wpf-data-binding-collection-properties-to-export-to-excel-in-vbnet.html and my Autodesk University class on WPF http://au.autodesk.com/?nd=material&session_material_id=5576

## 评论

**内容**: Tony Tanzillo said...
Hi Fenton.
Allowing the user to configure the foreground and background colors of the command line essentially requires that they also be able to configure the foreground and background colors of selected text, which isn't supported.
Reply
06/02/2013 at 04:42 PM

---
**内容**: Fenton Webb said...
Hi Tony
it is supported, it's just not WPF data-bound via this class at the moment. I'll logged it as a wish list for you, obviously.
Reply
06/03/2013 at 11:00 AM

---
**内容**: Craig said...
Hi Fenton,
What has happened to the AU class?
Regards
Craig
Reply
10/01/2013 at 08:50 AM

---
