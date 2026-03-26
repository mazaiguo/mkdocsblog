---
title: "Modify OSMODE mode in .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "GetsystemVariable and SetSystemVariable of the Application object can be used to access the OSMODE setting. Refer below .NET code"
author: Autodesk
---
# Modify OSMODE mode in .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/modify-osmode-mode-in-net.html

## 文章内容

By Virupaksha Aithal
GetsystemVariable and SetSystemVariable of the Application object can be used to access the OSMODE setting. Refer below .NET code
[CommandMethod("testOsnap")]
public static void testOsnap()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      Object obj = Application.GetSystemVariable("osmode");
    ed.WriteMessage("Current OSNAP : " + obj.ToString() + "\n");
    Application.SetSystemVariable("OSMODE", 2);
      //get the new OSNAP value..
    obj = Application.GetSystemVariable("osmode");
    ed.WriteMessage("OSNAP : " + obj.ToString() + "\n");
}

