---
title: "List all available plot styles with .NET API"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Database
  - Plot
description: "You need to iterate through the dictionary of plot style names in the Named Object Dictionary to find all plot styles available.  In the dictionary..."
author: Autodesk
---
# List all available plot styles with .NET API

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/list-all-available-plot-styles-with-net-api.html

## 文章内容

By Virupaksha Aithal
You need to iterate through the dictionary of plot style names in the Named Object Dictionary to find all plot styles available.  In the dictionary, each entry is a type of System.Collections.DictionaryEntry. Each DictionaryEntry object has a Key/Value pair of properties. The Key property is the name of the plot style and the value stores the Object ID of a PlaceHolder object.
[CommandMethod("ListPlotStyleName")]
static public void ListPlotStyleName()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId psDictId = db.PlotStyleNameDictionaryId;
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        DBDictionary dicObj = tr.GetObject(psDictId,
                                   OpenMode.ForRead) as DBDictionary;
          foreach (DBDictionaryEntry entry in dicObj)
        {
            //key will be name
            ed.WriteMessage(entry.Key + "\n");
              //entry.Value will have object id of  PlaceHolder
        }
          tr.Commit();
    }
}

## 评论

**内容**: Brent M. said...
This only lists plot styles that are currently being used. Any chance of finding a method to list ALL of the available plot styles, including those that haven't yet been used in the drawing?
Reply
05/21/2014 at 11:02 AM

---
