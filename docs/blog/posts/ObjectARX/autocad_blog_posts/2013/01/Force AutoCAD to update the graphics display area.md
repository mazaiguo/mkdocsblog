---
title: "Force AutoCAD to update the graphics display area"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "You can force the graphics update inserting the following lines in the code:"
author: Autodesk
---
# Force AutoCAD to update the graphics display area

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/force-autocad-to-update-the-graphics-display-area.html

## 文章内容

By Augusto Goncalves
You can force the graphics update inserting the following lines in the code:
actrTransactionManager->flushGraphics();
acedUpdateDisplay();
In the case where you use transactions to open entities and you have transaction(s) started, you then need to also call:
actrTransactionManager->queueForGraphicsFlush();
before calling the preceding functions.

## 评论

**内容**: Dan Plumley said...
Hi Augusto,
I am trying to prevent AutoCAD from updating the drawing screen while a VBA app runs. I would like run the VBA app and update the screen when the app completes.
Any idea how I might achieve this?
Many thanks,
Dan
Reply
11/22/2018 at 06:32 PM

---
**内容**: Augusto Goncalves said in reply to Dan Plumley...
Dan, with VBA every operation will trigger a regen, it's just how the COM API (ActiveX) works.
Reply
11/26/2018 at 03:32 PM

---
**内容**: David Sparks said...
Is there any way to force a regen (for example a newly copied viewport with layer overrides) from an active command in C# .net? The regen only happens when the command ends and I want the overrides in place after the viewport is copied and before other tasks continue.
Reply
12/11/2018 at 12:21 PM

---
**内容**: Madhukar Moogala said...
Can you try -
 vp.UpdateDisplay() 
Viewport.UpdateDisplay
This function updates the onscreen display to reflect any changes made to the viewport's view parameters. If no changes have been made, or the viewport is not on, or is not onscreen, then this function does nothing.
This function is automatically called when the viewport is closed, so the only time this function should need to be explicitly called is when the viewport is in a transaction and the onscreen graphics need to be updated before the outermost transaction is ended.
Reply
12/14/2018 at 09:12 PM

---
