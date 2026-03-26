---
title: "Quit AutoCAD"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "AutoCAD.NET API exposes “Application.Quit()” to exit the AutoCAD. However, “Application.Quit()” at present is unable to save all the user profile s..."
author: Autodesk
---
# Quit AutoCAD

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/quit-autocad.html

## 文章内容

By Virupaksha Aithal
AutoCAD.NET API exposes “Application.Quit()” to exit the AutoCAD. However, “Application.Quit()” at present is unable to save all the user profile setting (like active ribbon tab ). One alternative approach for the issue is to use quit AutoCAD command through “SendStringToExecute”   
[CommandMethod("quitACAD", CommandFlags.Session)]
static public void quitACAD()
{
    //Quit AutoCAD 
    Application.DocumentManager.MdiActiveDocument.SendStringToExecute("quit ", true, false, true);
}

## 评论

**内容**: Charles Ndung'u said...
very informative.thanks
Reply
07/10/2016 at 02:06 AM

---
