---
title: "GetPoint with Enter states "Invalid Point" instead of returning - Change in behavior"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - Plot
description: "I am using the GetPoint method. (AutoCAD COM interface using late binding). In AutoCAD 2010 and in previous versions hitting enter when prompted fo..."
author: Autodesk
---
# GetPoint with Enter states "Invalid Point" instead of returning - Change in behavior

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/getpoint-with-enter-states-invalid-point-instead-of-returning-change-in-behavior.html

## 文章内容

By Wayne Brill
Issue
I am using the GetPoint method. (AutoCAD COM interface using late binding). In AutoCAD 2010 and in previous versions hitting enter when prompted for a point would return. In 2011 instead of returning, "Invalid Point" is printed on the command line. Is there a way to allow Enter to return using GetPoint () in AutoCAD 2011 and later versions?
Solution
This change in behavior is considered to be correct. If you need Enter to be accepted with GetPoint make a call to InitializeUserInput(0) of the Utility object before using GetPoint().

## 评论

**内容**: Matus Brlit said...
you can also use Editor.GetPoint
with PromptPointOptions parameter
Dim ed As Editor = Autodesk.AutoCAD.ApplicationServices.Application.
DocumentManager.MdiActiveDocument.Editor
Dim optPoint As New PromptPointOptions("Your message")
optPoint.AllowNone = True
Dim resPoint As PromptPointResult = ed.GetPoint(optPoint)
Reply
05/28/2012 at 04:55 AM

---
