---
title: "Identifying the boundary through API"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - Database
description: "AutoCAD 2011 introduced a new API to identify the boundary objects for a provided point. Below code shows the use of the same API in .NET. The equi..."
author: Autodesk
---
# Identifying the boundary through API

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/identifying-the-boundary-through-api-.html

## 文章内容

By Virupaksha Aithal
AutoCAD 2011 introduced a new API to identify the boundary objects for a provided point. Below code shows the use of the same API in .NET. The equivalent ObjectARX API is “acedTraceBoundary”.
Note, only visible entities are considered while identifying the boundary objects.
[CommandMethod("BoundaryTest")]
public static void BoundaryTest()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   PromptPointOptions ptOptions =
                     new PromptPointOptions("Select point ");
 ptOptions.AllowNone = false;
 PromptPointResult ptResult = ed.GetPoint(ptOptions);
   if (ptResult.Status != PromptStatus.OK)
     return;
   DBObjectCollection collection =
                ed.TraceBoundary(ptResult.Value, true);
   using (Transaction Tx =
           db.TransactionManager.StartTransaction())
 {
     ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
        BlockTableRecord model = Tx.GetObject(ModelSpaceId,
                     OpenMode.ForWrite) as BlockTableRecord;
       foreach (DBObject obj in collection)
     {
         Entity ent = obj as Entity;
           if (ent != null)
         {
             //make the color as red.
             ent.ColorIndex = 1;
                model.AppendEntity(ent);
             Tx.AddNewlyCreatedDBObject(ent, true);
           }
     }
       Tx.Commit();
 }
}

## 评论

**内容**: Maxence said...
It seems that TraceBoundary only works in SCG:
var cucs = ed.CurrentUserCoordinateSystem;
try
{
ed.CurrentUserCoordinateSystem = Matrix3d.Identity;
collection = ed.TraceBoundary(point, true);
}
finally
{
ed.CurrentUserCoordinateSystem = cucs;
}
Reply
05/21/2013 at 09:45 AM

---
**内容**: Maxence said...
I mean WCS (SCG is for french) sorry.
Reply
05/21/2013 at 09:54 AM

---
**内容**: Parthiv said...
Hi,
I have drawn Some lines in one layer. A layer name is called "SteelBoundary"
All lines are connected. Now I want to find closest boundary only in this layer. How i can do. Some other lines also be there in other layers but I want to search only in
"SteelBoundary" layers
Thanks
Parthiv
Reply
10/23/2015 at 04:15 AM

---
**内容**: SpeedCAD said in reply to Parthiv...
I've seen this recently, and it occurs to me that you turn off all layers except the SteelBoundary layer, then apply TraceBoundary
Reply
04/30/2021 at 04:08 PM

---
