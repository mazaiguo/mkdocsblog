---
title: "Set ColumnType of MText on creation of MText Object"
date: 2018-04-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
  - Unicode
description: "We recently had a query regarding eNotApplicable runtime exception thrown trying to set ColumnType when MText is created as in the snippet:"
author: Autodesk
---
# Set ColumnType of MText on creation of MText Object

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/set-columntype-of-mtext-on-creation-of-mtext-object.html

## 文章内容

By Deepak Nadig
We recently had a query regarding eNotApplicable runtime exception thrown trying to set ColumnType when MText is created as in the snippet: 
MText mytext = new MText();
mytext.SetDatabaseDefaults();
mytext.Contents = "mytext";
mytext.Layer = "0";
mytext.ColorIndex = 3;
mytext.Location = new Point3d(0.0, 0.0, 0.0);
mytext.ColumnType = ColumnType.NoColumns;
To avoid this exception it is required to set MText.Width value greater than 0.0 before setting the ColumnType. Below command sets ColumnType 
[CommandMethod("TESTMTEXT")]
public static void testMtext()
{
    Document doc = Autodesk.AutoCAD.ApplicationServices.Core.Application.DocumentManager.MdiActiveDocument;
    if (doc == null)
        return;
    try
    {
        using (Transaction tr = doc.TransactionManager.StartTransaction())
        {
            MText mytext = new MText();
            mytext.SetDatabaseDefaults();
            mytext.Contents = "mytext";
            mytext.Layer = "0";
            mytext.ColorIndex = 3;
            mytext.Location = new Point3d(0.0, 0.0, 0.0);
            mytext.Width = 0.0; // don't forget me 
            if(mytext.Width > 0.0)
            mytext.ColumnType = ColumnType.NoColumns;

            BlockTable bt = (BlockTable)tr.GetObject(doc.Database.BlockTableId, OpenMode.ForRead);
            BlockTableRecord btr = (BlockTableRecord)tr.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite);
            btr.AppendEntity(mytext);
            tr.AddNewlyCreatedDBObject(mytext, true);
            tr.Commit();
        }
    }
    catch (System.Exception ex)
    {
        doc.Editor.WriteMessage("\nError: " + ex.ToString());
    }
}
It is notable that trying to change ColumnType of selected MText without setting Defined width value above 0.0 is not possible in UI :

## 评论

**内容**: Evgueny Fyodorov said...
Great thanx!
I myself would not have guessed.
Did so:
mText.Width = 1;
mText.ColumnType = ColumnType.NoColumns;
mText.Width = 0;
Reply
05/29/2020 at 01:51 AM

---
