---
title: "Finding all the visible raster images in the drawing."
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Database
description: "Here is a C# example that uses a filter to only select raster images in the drawing. It then iterates through those objects getting the RasterImage..."
author: Autodesk
---
# Finding all the visible raster images in the drawing.

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/finding-all-the-visible-raster-images-in-the-drawing.html

## 文章内容

By Virupaksha Aithal
Here is a C# example that uses a filter to only select raster images in the drawing. It then iterates through those objects getting the RasterImageDef and the layout they are on. 
  [CommandMethod("FindImages")]
public void findImages()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
    try
    {
        using (Transaction tr =
                db.TransactionManager.StartTransaction())
        {
            TypedValue[] filterlist = new TypedValue[1];
            filterlist[0] = new TypedValue(0, "IMAGE");
            SelectionFilter filter =
                            new SelectionFilter(filterlist);
              PromptSelectionResult selRes = ed.SelectAll(filter);
              if (selRes.Status != PromptStatus.OK)
            {
                ed.WriteMessage("\nNo Images selected");
                return;
            }
              SelectionSet oSS = selRes.Value;
            ed.WriteMessage("\nNumber of raster images in dwg "
                                        + oSS.Count.ToString());
              //Iterate through the selectionset
            for (int i = 0; i < oSS.Count; i++)
            {
                RasterImage oRaster;
                oRaster = (RasterImage)tr.GetObject(oSS[i].ObjectId,
                                            OpenMode.ForRead);
                ed.WriteMessage("\nBlock name = " +
                                      oRaster.BlockName.ToString());
                BlockTableRecord oBlkTblRec =
                    (BlockTableRecord)tr.GetObject(oRaster.BlockId,
                                                 OpenMode.ForRead);
                  if (oBlkTblRec.IsLayout)
                {
                    Layout lyt =
                            (Layout)tr.GetObject(oBlkTblRec.LayoutId,
                                                 OpenMode.ForRead);
                    RasterImageDef oRasterIDef =
                     (RasterImageDef)tr.GetObject(oRaster.ImageDefId,
                                                  OpenMode.ForRead);
                    ed.WriteMessage("\nRaster image "
                        + oRasterIDef.ActiveFileName.ToString() +
                            " is on a layout named: " +
                               lyt.LayoutName.ToString());
                }
            }
            tr.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.ToString());
    }
}

## 评论

**内容**: Philip said...
Could you tell me which imports i do need? :)
Reply
08/08/2012 at 08:24 AM

---
