---
title: "Getting material name associated with a face"
date: 2012-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Solid
description: "In AutoCAD, each face of a solid can be assigned a material. To get the material name of a face, you will first need to traverse the faces of the S..."
author: Autodesk
---
# Getting material name associated with a face

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/getting-material-name-associated-with-a-face.html

## 文章内容

By Balaji Ramamoorthy
In AutoCAD, each face of a solid can be assigned a material. To get the material name of a face, you will first need to traverse the faces of the Solid3D. Here is a sample code :
Document activeDoc =
        Application.DocumentManager.MdiActiveDocument;
  Database db = activeDoc.Database;
Editor ed = activeDoc.Editor;
  PromptEntityOptions peo =
        new PromptEntityOptions("\nSelect a Solid3d : ");
peo.SetRejectMessage("\nPlease select a Solid3d...");
peo.AddAllowedClass(typeof(Solid3d), true);
  PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK)
    return;
  using (Transaction tr =
        db.TransactionManager.StartTransaction())
{
    Solid3d solid3d = tr.GetObject(
          per.ObjectId, OpenMode.ForWrite) as Solid3d;
      ObjectId[] ids = new ObjectId[] { solid3d.ObjectId };
    FullSubentityPath path =
        new FullSubentityPath(ids,
                    new SubentityId(SubentityType.Null,
                     IntPtr.Zero));
      using (Brep brep = new Brep(path))
    {
        foreach
        (
            Autodesk.AutoCAD.BoundaryRepresentation.Face
            face in brep.Faces
        )
        try
        {
            ObjectId materialId
                = solid3d.GetSubentityMaterial(
                        face.SubentityPath.SubentId);
                Material material =
                        tr.GetObject(materialId,
                        OpenMode.ForRead) as Material;
               ed.WriteMessage("\n" + material.Name);
         }
         catch (System.Exception ex)
         {
             ed.WriteMessage(ex.Message);
         }
    }
    tr.Commit();
}

## 评论

**内容**: trung doo said...
Hi,
i used to your code above, but they have a problem with my program message error. You can see attached message below:
Select a Solid3d: eDeletedEntryeDeletedEntryeDeletedEntryeDeletedEntryeDeletedEntryeDeletedEntry
Reply
11/28/2016 at 08:24 PM

---
