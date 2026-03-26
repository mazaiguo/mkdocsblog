---
title: "Listing all the table styles in a drawing"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Plot
description: "Table styles are stored in named object dictionary under table style dictionary. Below code shows the procedure to traverse the table style diction..."
author: Autodesk
---
# Listing all the table styles in a drawing

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/listing-all-the-table-styles-in-a-drawing.html

## 文章内容

By Virupaksha Aithal
Table styles are stored in named object dictionary under table style dictionary. Below code shows the procedure to traverse the table style dictionary. The code also prints the current table style name.
[CommandMethod("ListTableStyles")]
static public void ListTableStyles()
{
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId tsId = ObjectId.Null;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        DBDictionary tsd = (DBDictionary)tr.GetObject(
                                            db.TableStyleDictionaryId,
                                                    OpenMode.ForRead);
          TableStyle tStyle = null;
        foreach (DBDictionaryEntry entry in tsd)
        {
            tStyle = (TableStyle)tr.GetObject(entry.Value,
                                                    OpenMode.ForRead);
              ed.WriteMessage(tStyle.Name + "\n");
        }
        //current table style
        tStyle = (TableStyle)tr.GetObject(
                                db.Tablestyle, OpenMode.ForRead);
        ed.WriteMessage("Current table style: " + tStyle.Name+"\n");
        tr.Commit();
    }
}

