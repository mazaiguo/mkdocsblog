---
title: "Creating a new table style"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "Below code shows the procedure to create a new table style. Newly created table style is added to database using API “PostTableStyleToDatabase”. Th..."
author: Autodesk
---
# Creating a new table style

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-a-new-table-style.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to create a new table style. Newly created table style is added to database using API “PostTableStyleToDatabase”. The code also makes the new table style as current table style of the database.
[CommandMethod("NewTableStyle")]
static public void NewTableStyle()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   ObjectId tsId = ObjectId.Null;
   using (Transaction tr =
                    db.TransactionManager.StartTransaction())
 {
     //Name of the Table Style to create
     const string styleName = "TestTableStyle";
       DBDictionary tsd = (DBDictionary)tr.GetObject(
                             db.TableStyleDictionaryId,
                             OpenMode.ForRead);
         if (!tsd.Contains(styleName))
     {
         //now get the active table style
         TableStyle currentStyle = tr.GetObject(db.Tablestyle,
                              OpenMode.ForRead) as TableStyle;
         TableStyle newStyle =
                            currentStyle.Clone() as TableStyle;
           // now set the values of new table Style...
             tsId = newStyle.PostTableStyleToDatabase(db,
                                                styleName);
         tr.AddNewlyCreatedDBObject(newStyle, true);
           //make the style as current
         db.Tablestyle = tsId;
     }
       tr.Commit();
 }
}

