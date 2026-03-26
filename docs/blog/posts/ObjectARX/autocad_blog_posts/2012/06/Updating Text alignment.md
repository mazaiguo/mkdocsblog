---
title: "Updating Text alignment"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Plugin
  - Unicode
description: "Under certain conditions, the text alignment set to a DBText does not take effect. To ensure that the alignment is correct, the "DBText.AdjustAlign..."
author: Autodesk
---
# Updating Text alignment

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/updating-text-alignment-.html

## 文章内容

By Balaji Ramamoorthy
Under certain conditions, the text alignment set to a DBText does not take effect. To ensure that the alignment is correct, the "DBText.AdjustAlignment" method is to be used. This method makes use of the working database internally for its working. So, it is important to set the working database if the database to which the DBText is being added is not already the working database.
Here is a sample code :
[CommandMethod("TextAlign")]
public void TextAlign()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
      // For adding a text with alignment to the current document
    bool isInMemory = false;
    Database db = activeDoc.Database;
      // For adding a text to an in-memory database
    //bool isInMemory = true;
    //Database db = new Database(true, false);
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord mSpace = tr.GetObject
                                (
                                    bt[BlockTableRecord.ModelSpace],
                                    OpenMode.ForWrite
                                ) as BlockTableRecord;
          DBText dbText = new DBText();
        dbText.SetDatabaseDefaults(db);
          dbText.Position = Point3d.Origin;
        dbText.Height = 5.0;
        dbText.TextString = "Autodesk";
        dbText.HorizontalMode = TextHorizontalMode.TextRight;
        dbText.AlignmentPoint = Point3d.Origin;
          if (isInMemory)
        {   // For adding a text with an alignment to an in-memory database
            // set the working database before using AdjustAlignment
            Database prevWorkingDb = HostApplicationServices.WorkingDatabase;
            HostApplicationServices.WorkingDatabase = db;
            dbText.AdjustAlignment(db);
            HostApplicationServices.WorkingDatabase = prevWorkingDb;
        }
        else
        {   // For adding a text with alignment to the current document
            // working database is already set
            dbText.AdjustAlignment(db);
        }
          mSpace.AppendEntity(dbText);
        tr.AddNewlyCreatedDBObject(dbText, true);
          tr.Commit();
    }
      if (isInMemory)
    {
        db.SaveAs("C:\\Temp\\Test.dwg", DwgVersion.Current);
        db.Dispose();
    }
}

## 评论

**内容**: Angel Star said...
Sorry for my poor English(From China).I'm trying to add some texts in a new document(not current document),and however I tried to set the texts to the wanted positions,they always turn out to be in the origin position(coordinates(0,0)).Only after I double click them,then they move to the correct-set positions.I look up books and information,just cannot solve the problem,can you help me?Down blew is part of my codes.Looking forward to your help.Thanks a lot!
using (Transaction trans = NewDoc.Database.TransactionManager.StartTransaction())
{
BlockTable bt = trans.GetObject(NewDoc.Database.BlockTableId, OpenMode.ForRead) as BlockTable;
BlockTableRecord btr = trans.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite) as BlockTableRecord;
DBText BoldTst;
BoldTst = new DBText();
BoldTst.SetDatabaseDefaults(NewDoc.Database);
//BoldTst.Position = new Point3d(PFLst[i].LefTop.X + 125, PFLst[i].LefTop.Y + 14.00, 0);
BoldTst.HorizontalMode = TextHorizontalMode.TextCenter;
BoldTst.VerticalMode = TextVerticalMode.TextVerticalMid;
BoldTst.AlignmentPoint = new Point3d(PFLst[i].LefTop.X + 125, PFLst[i].LefTop.Y + 14.00, 0);
BoldTst.ColorIndex = 7;
BoldTst.Height = 3.00;
BoldTst.WidthFactor = 1.0;
BoldTst.TextString = "福清市" + DistrictName + "地籍图";
BoldTst.AdjustAlignment(NewDoc.Database);
btr.AppendEntity(BoldTst);
trans.AddNewlyCreatedDBObject(BoldTst, true);
trans.Commit();
}
Reply
12/25/2017 at 04:43 PM

---
**内容**: Hans Martin Eikerol said...
Thanks alot! Worked like a charm!
Reply
09/06/2018 at 04:41 AM

---
**内容**: badziewiak said...
@Balaji Ramamoorthy
Thank you very very much!!!
Reply
08/18/2019 at 06:00 AM

---
