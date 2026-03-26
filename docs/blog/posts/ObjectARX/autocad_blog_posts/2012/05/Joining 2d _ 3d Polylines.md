---
title: "Joining 2d / 3d Polylines"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "Here is a sample code that uses the "Entity.JoinEntity" method to demonstrate joining of 2d/3d polylines"
author: Autodesk
---
# Joining 2d / 3d Polylines

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/joining-2d-3d-polylines.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code that uses the "Entity.JoinEntity" method to demonstrate joining of 2d/3d polylines
[CommandMethod("joinPline")]
static public void joinPolylines()
{
    Document document =
                Application.DocumentManager.MdiActiveDocument;
    Editor ed = document.Editor;
    Database db = document.Database;
      PromptEntityOptions peo1
        = new PromptEntityOptions("\nSelect source polyline : ");
      peo1.SetRejectMessage("\nInvalid selection...");
      peo1.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline),
            true
        );
      peo1.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline2d),
            true
        );
      peo1.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline3d),
            true
        );
      PromptEntityResult pEntrs = ed.GetEntity(peo1);
    if (PromptStatus.OK != pEntrs.Status)
        return;
      ObjectId srcId = pEntrs.ObjectId;
      PromptEntityOptions peo2
        = new PromptEntityOptions("\nSelect polyline to join : ");
      peo2.SetRejectMessage("\nInvalid selection...");
    peo2.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline),
            true
        );
      peo2.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline2d),
            true
        );
      peo2.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline3d),
            true
        );
      pEntrs = ed.GetEntity(peo2);
    if (PromptStatus.OK != pEntrs.Status)
        return;
      ObjectId joinId = pEntrs.ObjectId;
    try
    {
        using (Transaction trans
            = db.TransactionManager.StartTransaction())
        {
            Entity srcPLine
                = trans.GetObject(
                                    srcId,
                                    OpenMode.ForRead
                                 ) as Entity;
              Entity addPLine
                = trans.GetObject(
                                    joinId,
                                    OpenMode.ForRead
                                  ) as Entity;
              srcPLine.UpgradeOpen();
            srcPLine.JoinEntity(addPLine);
              addPLine.UpgradeOpen();
            addPLine.Erase();
              trans.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}

## 评论

**内容**: Viacheslav said...
Thanks a lot for your post!
Reply
04/14/2015 at 09:59 PM

---
**内容**: Paojie said...
Tks a lot
It is very Useful
Reply
04/15/2015 at 06:12 AM

---
**内容**: viswanathan said...
This is excellent code. It is very useful.
Reply
09/12/2017 at 09:24 PM

---
**内容**: Ravi said...
Hello Balaji,
When am going to join two lines it's throwing error as "eNotApplicable".Can you suggest me how to find out the solution.If you have any code please let me know.
Reply
02/07/2019 at 09:09 AM

---
