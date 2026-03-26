---
title: "Converting Polyline to Polyline2d"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Polyline
description: "There is a method called Polyline.ConvertTo that can convert a lightweight polyline into a polyline 2d object, but this method requires a special t..."
author: Autodesk
---
# Converting Polyline to Polyline2d

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/converting-polyline-to-polyline2d.html

## 文章内容

By Augusto Goncalves
There is a method called Polyline.ConvertTo that can convert a lightweight polyline into a polyline 2d object, but this method requires a special treatment.
First, it is required to use StartOpenCloseTransaction method to create a new transaction, instead regular StartTransaction. Second, remove the old polyline and append the newly created polyline 2d.
ObjectId plineId = // obtain here...
Database db =
  Application.DocumentManager.MdiActiveDocument.Database;
using (Transaction t =
  db.TransactionManager.StartOpenCloseTransaction())
{
  using (Polyline pline = (Polyline)
    t.GetObject(plineId, OpenMode.ForWrite))
  {
    t.AddNewlyCreatedDBObject(pline, false);
    Polyline2d poly2 = pline.ConvertTo(true);
    t.AddNewlyCreatedDBObject(poly2, true);
    t.Commit();
  }
}

## 评论

**内容**: Maxence said...
Thanks. I finally know for why the second argument of AddNewlyCreatedDBObject exists.
Reply
08/04/2014 at 02:50 AM

---
