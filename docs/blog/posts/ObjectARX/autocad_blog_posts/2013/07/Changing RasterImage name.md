---
title: "Changing RasterImage name"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Palette
description: "The name field displayed in the property palette for a RasterImage is obtained by AutoCAD from the dictionary entry used to store its RasterImageDe..."
author: Autodesk
---
# Changing RasterImage name

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/changing-rasterimage-name.html

## 文章内容

By Balaji Ramamoorthy
The name field displayed in the property palette for a RasterImage is obtained by AutoCAD from the dictionary entry used to store its RasterImageDef in the "ACAD_IMAGE_DICT" named object dictionary. To change the name of a RasterImage, we can create a new RasterImageDef and associate all the existing RasterImages to it. Also, it is important to disable RasterImage reactors while the old RasterImageDef is being unloaded and erased.
Here is a sample code :
Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
  PromptStringOptions pso1
        = new PromptStringOptions("\nEnter old image name : ");
pso1.AllowSpaces = true;
PromptResult pr1 = ed.GetString(pso1);
if (pr1.Status != PromptStatus.OK)
    return;
String oldImageName = pr1.StringResult;
  PromptStringOptions pso2
        = new PromptStringOptions("\nEnter new image name : ");
pso2.AllowSpaces = true;
PromptResult pr2 = ed.GetString(pso2);
if (pr2.Status != PromptStatus.OK)
    return;
String newImageName = pr2.StringResult;
  ObjectId oldridId = ObjectId.Null;
ObjectId newridId = ObjectId.Null;
  using (Transaction tr = db.TransactionManager.StartTransaction())
{
    ObjectId dictId = RasterImageDef.GetImageDictionary(db);
    if (! dictId.IsNull)
    {
        DBDictionary dict = tr.GetObject(
                                            dictId,
                                            OpenMode.ForRead
                                        ) as DBDictionary;
        if (dict.Contains(oldImageName))
        {
            // Step 1: Create a new RasterImageDef based on
            // the old RasterImageDef
            oldridId = dict.GetAt(oldImageName);
            RasterImageDef oldrid = tr.GetObject(
                                                    oldridId,
                                                    OpenMode.ForWrite
                                                ) as RasterImageDef;
            RasterImageDef newrid = new RasterImageDef();
              newrid.SourceFileName = oldrid.SourceFileName;
            newrid.ActiveFileName = oldrid.ActiveFileName;
            newrid.Load();
            dict.UpgradeOpen();
            newridId = dict.SetAt(newImageName, newrid);
            tr.AddNewlyCreatedDBObject(newrid, true);
              // Step 2: Associate the existing raster images
            // with the newly created RasterImageDef
            RasterImage.EnableReactors(true);
              BlockTable bt = tr.GetObject(
                                            db.BlockTableId,
                                            OpenMode.ForRead
                                        ) as BlockTable;
            foreach (ObjectId btrId in bt)
            {
                BlockTableRecord btr = tr.GetObject
                                        (
                                            btrId,
                                            OpenMode.ForRead
                                        ) as BlockTableRecord;
                foreach (ObjectId id in btr)
                {
                    if (id.ObjectClass.IsDerivedFrom(
                        RXClass.GetClass(typeof(RasterImage))))
                    {
                        RasterImage ri = tr.GetObject
                                            (
                                                id,
                                                OpenMode.ForRead
                                            ) as RasterImage;
                        if (ri.ImageDefId.Equals(oldridId))
                        {
                            ri.UpgradeOpen();
                            ri.AssociateRasterDef(newrid);
                            ri.ImageDefId = newridId;
                        }
                    }
                }
            }
              // Step 3 : Detach and erase the old RasterImageDef
            RasterImage.EnableReactors(false);
            oldrid.Unload(true);
            oldrid.Erase();
        }
    }
    tr.Commit();
}
  // Resolve Xrefs
db.ResolveXrefs(false, false);

## 评论

**内容**: Youssef said...
Thank you very much Balaji.
Reply
12/22/2020 at 05:23 AM

---
