---
title: "AcCoreConsole: Explode DBText To Geometry"
date: 2018-04-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Database
  - Forge
  - Polyline
  - Unicode
description: "I received a query from one of our Technical Sales Specialist whose customer would like to automate a design workflow using Forge Design Automation..."
author: Autodesk
---
# AcCoreConsole: Explode DBText To Geometry

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/accoreconsole-explode-dbtext-to-geomety.html

## 文章内容

By Madhukar Moogala
I received a query from one of our Technical Sales Specialist whose customer would like to automate a design workflow using Forge Design Automation one aspect of work flow is to explode Text objects in to Geometry [polylines and arcs].
We have an existing express tool called TXTEXP, unfortunately this tool is not available for Forge or AcCoreConsole, I created a simple C# program which explodes a text object in to geometry, this custom program can be used as custom command in AcCoreConsole.

public void EXPTXT()
{
    var doc = Application.DocumentManager.MdiActiveDocument;
    var db = doc.Database;
    var ed = doc.Editor;
    // selection text
    ObjectId[] dbtextIds = ed.SelectTextEntitesInModelSpace();
    foreach (ObjectId id in dbtextIds)
    {
        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
            var text = (DBText)tr.GetObject(id, OpenMode.ForWrite);
            ObjectId[] ids = new ObjectId[1];
            ids[0] = id;
            ed.SetImpliedSelection(ids);
            var tempFile = Path.Combine(Path.GetTempPath(), "Q.wmf");

            if (File.Exists(tempFile))
            {
                File.Delete(tempFile);
            }
            ed.Command("_.WMFOUT", tempFile, "", "");
            var viewSize = (double)Application.GetSystemVariable("VIEWSIZE");
            var screenSize = (Point2d)Application.GetSystemVariable("SCREENSIZE");
            double factor = viewSize * (screenSize.X / screenSize.Y);
            var viewCtr = (Point3d)Application.GetSystemVariable("VIEWCTR");
            //Transform viewCtr from UCS to DCS
            Matrix3d matUCS2DCS = ed.UCS2WCS() * ed.WCS2DCS();
            viewCtr = viewCtr.TransformBy(matUCS2DCS);
            var p1 = new Point3d(viewCtr.X - (factor / 2.0), 
                                 viewCtr.Y - (viewSize / 2.0), .0);
            var p2 = new Point3d(viewCtr.X + (factor / 2.0),
                                viewCtr.Y + (viewSize / 2.0), .0);
            //Transorm p1,p2 from DCS to UCS;
            Matrix3d matDCS2UCS = ed.DCS2WCS() * ed.WCS2UCS();
            p1 = p1.TransformBy(matDCS2UCS);
            p2 = p2.TransformBy(matDCS2UCS);
            Point2d wmfinBlockPos = new Point2d(p1.X, p2.Y);
            var tempWithOutExt = Path.Combine(Path.GetDirectoryName(tempFile),
                                 Path.GetFileNameWithoutExtension(tempFile));
            ed.Command("_.WMFIN", tempWithOutExt, wmfinBlockPos, "2", "", "");
            try
            {
                var wmfBlock = tr.GetObject(ed.SelectLastEnt(), OpenMode.ForWrite) as BlockReference;
                DBObjectCollection pElems = new DBObjectCollection();
                wmfBlock?.Explode(pElems);
                var space = (BlockTableRecord)tr.GetObject(db.CurrentSpaceId, OpenMode.ForWrite);
                foreach (DBObject elem in pElems)
                {
                    space.AppendEntity(elem as Entity);
                    tr.AddNewlyCreatedDBObject(elem, true);
                }
                //Purge unused WMFIN Block and reference
                ObjectId wmfBtr = GetNonErasedTableRecordId(db.BlockTableId, wmfBlock.Name);
                ObjectIdCollection blockIds = new ObjectIdCollection();
                blockIds.Add(wmfBtr);
                db.Purge(blockIds);
                foreach (ObjectId oId in blockIds)
                {
                    DBObject obj = tr.GetObject(oId, OpenMode.ForWrite);
                    obj.Erase();

                }
            }
            catch (Exception ex)
            {
                ed.WriteMessage(ex.Message);
            }
            finally
            {
                //Erase text entity
                text.Erase();
                tr.Commit();
            }
        }

    }

}
source:
Explode-Text-To-Geomety
Preview In Action
via GIPHY

## 评论

**内容**: Olivier said...
Hello,
it works if the text style height is different from 1.0
Reply
04/13/2018 at 05:12 AM

---
**内容**: Madhukar Moogala said in reply to Olivier...

Typepad HTML Email

Olivier,
 
Thanks for stopping by
😊
I believe it should, I have not done robust testing on sample, this is to get start.
Please feel free download the source code and try it out ;), I am happy accept any pull requests
  Reply
04/13/2018 at 05:29 AM

---
**内容**: Madhukar Moogala said...
Hi,
I have tested changing the style scale to other than 1, it works correctly.
The test drawing in consideration is here.
https://autodesk.box.com/v/ExpTxt-2018
Reply
04/13/2018 at 06:55 AM

---
