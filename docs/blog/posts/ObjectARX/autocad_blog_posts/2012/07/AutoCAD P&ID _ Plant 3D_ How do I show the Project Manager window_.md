---
title: "AutoCAD P&ID / Plant 3D: How do I show the Project Manager window?"
date: 2012-07-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Palette
  - Plant 3D
description: "I would like to show the Project Manager palette programmatically, if it’s hidden. Can I do this?"
author: Autodesk
---
# AutoCAD P&ID / Plant 3D: How do I show the Project Manager window?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/autocad-pid-plant-3d-how-do-i-show-the-project-manager-window.html

## 文章内容

By Marat Mirgaleev
Issue
I would like to show the Project Manager palette programmatically, if it’s hidden. Can I do this?
Solution
There is an undocumented command called "_REFRESHPMESW" that shows the Project Manager. So, we can simply call that command with these lines of code:
  Document doc = Application.DocumentManager.MdiActiveDocument;
  doc.SendStringToExecute("_REFRESHPMESW ", true, false, true );    
The "_REFRESHPMESW" command also refreshes the information in the window. It may be helpful when your program changes the project structure.

