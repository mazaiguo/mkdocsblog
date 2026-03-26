---
title: "Can I Run AutoCAD P&ID/Plant 3D in Console Mode?"
date: 2012-10-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
description: "I would like to do some batch processing in AutoCAD Plant 3D. May I use AcCoreConsole.exe for it?"
author: Autodesk
---
# Can I Run AutoCAD P&ID/Plant 3D in Console Mode?

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/can-i-run-autocad-pidplant-3d-in-console-mode.html

## 文章内容

By Marat Mirgaleev
Issue
I would like to do some batch processing in AutoCAD Plant 3D. May I use AcCoreConsole.exe for it?
Solution
For Plant 3D it should work, but with some limitations, of course:
1) In the Windows Explorer, go to the C:\Program Files\Autodesk\AutoCAD Plant 3D 2013 – English;
2) Start AcCoreConsole.exe;
3) Load the Object Enablers – type in the command line:
     arx
     L
     PnP3dObjects.dbx
I should clarify that the Plant 3D Object Enablers work, but the “Plant Environment” is full of ARX apps that will not load into AcCoreConsole.exe. Therefore, none of the PLANT product’s commands are available.
Unfortunately, the same approach will not work for AutoCAD P&ID, since it does not have Object Enablers usable outside of AutoCAD.
I want to say “Thank you” to Jorge Lopez from the Plant development team for his infinite help in answering questions like this!

