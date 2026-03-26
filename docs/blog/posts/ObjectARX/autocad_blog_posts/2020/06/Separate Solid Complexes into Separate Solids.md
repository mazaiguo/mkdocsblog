---
title: "Separate Solid Complexes into Separate Solids"
date: 2020-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Solid
description: "You can try using Solid3d.SeparateBody Method"
author: Autodesk
---
# Separate Solid Complexes into Separate Solids

发布日期: 2020-06-01

原始链接: https://adndevblog.typepad.com/autocad/2020/06/separate-solid-complexes-into-separate-solids.html

## 文章内容

By Madhukar Moogala
You can try using Solid3d.SeparateBody Method
This method separates the solid into a list of solids representing the additional disjoint volumes.
This solid is reduced to a solid with one volume.
The calling application is responsible for the resulting entities (either appending them to a database or deleting them when they are no longer needed).
When the calling application closes this Solid3d, the resulting solid will be committed to the database.
So, if the other solids are not appended to the database, you will lose some data.
To separate solids interactively in UI, refer this knowledge article.
Please note, you need a Solid which is logical one, but visually it appears to be two or more, i.e, you can move or copy multiple disjoint solids as one.
I have attached one drawing.

public static void SepSolid()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
PromptEntityOptions peo = new PromptEntityOptions("\nSelect solid:");
peo.SetRejectMessage("\nMust be a 3D solid.");
peo.AddAllowedClass(typeof(Solid3d), false);
PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK) return;
Transaction tr = db.TransactionManager.StartTransaction();
using (tr)
{
Solid3d sol = tr.GetObject(per.ObjectId, OpenMode.ForRead)
as Solid3d;
if (sol != null)
{
sol.UpgradeOpen();
//The solid must have multiple lumps
Solid3d[] disjointSolids = sol.SeparateBody();
foreach (Solid3d v in disjointSolids)
{
    Vector3d dispVector = Point3d.Origin.GetVectorTo(v.MassProperties.Centroid);
    v.TransformBy(Matrix3d.Displacement(dispVector));
    v.ColorIndex = 3;
    using (OpenCloseTransaction oct = new OpenCloseTransaction())
    {
        // Open the Block table for read
        BlockTable acBlkTbl;
        acBlkTbl = oct.GetObject(db.BlockTableId,
                                            OpenMode.ForRead) as BlockTable;
        // Open the Block table record Model space for write
        BlockTableRecord acBlkTblRec;
        acBlkTblRec = oct.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                                OpenMode.ForWrite) as BlockTableRecord;
        acBlkTblRec.AppendEntity(v);
        oct.AddNewlyCreatedDBObject(v, true);
        // Save the new objects to the database
        oct.Commit();
    }
}
}
tr.Commit();

}
}
Demo

## 评论

**内容**: Khoi Tran said...
Dear Madhukar Moogala
Sorry for inconvenience. I have problem need some help from you.
I use RealDWG lib to read .dwg file and render it on my application.
I use some code from post https://forums.autodesk.com/t5/objectarx/triangulating-3d-solids/td-p/9618472, and rendered it's geometry on my application.
But with AcDb3dsolid that contain a texture image file, i want to apply texture on polygon. however i don't find solution to do it.
I want to extract something like AcDbSubDMesh::getVertexTextureArray(AcGePoint3dArray &arr). With AcDbSubDMesh i can apply texture on polygon.
Can you help me point out something to resolve this problem.
Thanks you,
Reply
07/14/2021 at 01:05 AM

---
