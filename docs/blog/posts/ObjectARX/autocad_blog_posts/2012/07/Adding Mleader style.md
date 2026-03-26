---
title: "Adding Mleader style"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
  - Plugin
description: "Mleader styles are stored under a NOD named “ACADMLEADERSTYLE”. You can directly get the object id of this dictionary using database property “MLea..."
author: Autodesk
---
# Adding Mleader style

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/adding-mleader-style-.html

## 文章内容

By Virupaksha Aithal
Mleader styles are stored under a NOD named “ACAD_MLEADERSTYLE”. You can directly get the object id of this dictionary using database property “MLeaderStyleDictionaryId”. Below code shows the procedure to add a new mleader style to database. The code also makes it current by setting the database property “MLeaderstyle”.
[CommandMethod("AddMleaderStyle")]
static public void AddMleaderStyle()
{
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr =
                       db.TransactionManager.StartTransaction())
    {
        //Name of the mleader Style to edit
        const string styleName = "Test";
          DBDictionary mlstyles = (DBDictionary)tr.GetObject(
                                        db.MLeaderStyleDictionaryId,
                                        OpenMode.ForRead);
          ObjectId mLeaderStyle = ObjectId.Null;
          if (!mlstyles.Contains(styleName))
        {
           //add a new mleader style...
            MLeaderStyle newStyle = new MLeaderStyle();
              //make the arrow head as DOT.
            BlockTable blockTable = tr.GetObject(db.BlockTableId,
                                OpenMode.ForRead) as BlockTable;
            if (!blockTable.Has("_DOT"))
            {
                //load
                Application.SetSystemVariable("DIMBLK", "_DOT");
            }
            //now set the arrow hear.
            newStyle.ArrowSymbolId = blockTable["_DOT"];
              mLeaderStyle =
                newStyle.PostMLeaderStyleToDb(db, styleName);
            tr.AddNewlyCreatedDBObject(newStyle, true);
        }
        else
        {
            mLeaderStyle = mlstyles.GetAt(styleName);
        }
          //make the new leader as current...
        db.MLeaderstyle = mLeaderStyle;
        tr.Commit();
    }
}

## 评论

**内容**: Rick said...
Is it possible to have this example in ObjectARX C++
Reply
10/15/2020 at 12:11 AM

---
