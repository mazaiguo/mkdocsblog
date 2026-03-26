---
title: "Annotation scale being used in Model Space"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Database
description: "I'm trying to get back the annotation scale being used in Model Space."
author: Autodesk
---
# Annotation scale being used in Model Space

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/annotation-scale-being-used-in-model-space.html

## 文章内容

By Adam Nagy
I'm trying to get back the annotation scale being used in Model Space.
The below picture shows what I'm looking for:

Solution
If you change the Annotation Scale value in Model Space, then you'll see that the _CANNOSCALE command is being used in the background. Now if you look for that name in the Visual Studio Object Browser, then you'll find Database.Cannoscale, which is the variable you are looking for:
[CommandMethod("AEN1GetAnnotationScale")]
static public void AEN1GetAnnotationScale()
{
  Database db = HostApplicationServices.WorkingDatabase;
  Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.
    DocumentManager.MdiActiveDocument.Editor;
    ed.WriteMessage(
    "Current annotation scale is: " + db.Cannoscale.Name + "\n");
}

