---
title: "Creating a 3 point Angular Dimension using Point3AngularDimension in .NET"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - Dimension
description: "The Point3AngularDimension class in AutoCAD .NET API helps to create a 3 point angular dimension. Following Code snippet explains how to create a 3..."
author: Autodesk
---
# Creating a 3 point Angular Dimension using Point3AngularDimension in .NET

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/creating-a-3-point-angular-dimension-using-point3angulardimension-in-net.html

## 文章内容

By Virupaksha Aithal
The Point3AngularDimension class in AutoCAD .NET API helps to create a 3 point angular dimension. Following Code snippet explains how to create a 3 point angular dimension for an ARC entity.
[CommandMethod("netDimAngular")]
public void netDimAngular()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   PromptEntityOptions peo = new
        PromptEntityOptions("\nSelect an Arc: ");
   peo.SetRejectMessage("\nMust be an Arc...");
 peo.AddAllowedClass(typeof(Arc), true);
 PromptEntityResult per = ed.GetEntity(peo);
   if (per.Status != PromptStatus.OK)
     return;
   using (Transaction Tx =
        db.TransactionManager.StartTransaction())
 {
     Arc arc = Tx.GetObject(per.ObjectId
                        , OpenMode.ForRead) as Arc;
     BlockTable bt = Tx.GetObject(db.BlockTableId,
                        OpenMode.ForRead) as BlockTable;
     BlockTableRecord btr = Tx.GetObject(
                            bt[BlockTableRecord.ModelSpace],
                        OpenMode.ForWrite) as BlockTableRecord;
     string dimStyle = "Standard";
     DimStyleTable dimStyleTable = Tx.GetObject(
                                  db.DimStyleTableId,
                               OpenMode.ForRead) as DimStyleTable;
       if (dimStyleTable.Has(dimStyle))
     {
         Point3d point3 =
              arc.StartPoint.Add(
                    arc.EndPoint.GetAsVector()).MultiplyBy(0.5);
           ObjectId dimStyleId = dimStyleTable[dimStyle];
         Point3AngularDimension dim = new
          Point3AngularDimension(arc.Center,
                            arc.StartPoint,
                            arc.EndPoint,
                            point3, "",
                            dimStyleId);
           btr.AppendEntity(dim);
         Tx.AddNewlyCreatedDBObject(dim, true);
         Tx.Commit();
     }
 }
}

## 评论

**内容**: Fuse Angular said...
A dofollow value is simply a descriptor since a dofollow value for the rel attribute doesn’t exist in HTML. So, dofollow links are technically any links that don’t have an rel attribute with a nofollow value.
Reply
04/12/2019 at 09:30 AM

---
