---
title: "Identifying the presence of registered application name in Xdata of the entity"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "You can use DBobject  API “GetXDataForApplication” to identify the presence of Xdata of particular application name. Below code shows the same use ..."
author: Autodesk
---
# Identifying the presence of registered application name in Xdata of the entity

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/identifying-the-presence-of-registered-application-name-in-xdata-of-the-entity.html

## 文章内容

By Virupaksha Aithal
You can use DBobject  API “GetXDataForApplication” to identify the presence of Xdata of particular application name. Below code shows the same use of “GetXDataForApplication” API to identify the presence of “ADSK” registered application name.
[CommandMethod("FindAppName")]
static public void FindAppName() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Transaction tr = db.TransactionManager.StartTransaction();
    using (tr)
    {
        Editor ed = doc.Editor;
        try
        {
           PromptEntityResult ers = ed.GetEntity("Pick entity ");
           Entity ent = (Entity)tr.GetObject(ers.ObjectId,
                                               OpenMode.ForRead);
              ResultBuffer buffer =
                ent.GetXDataForApplication("ADSK");
              //if null no xdata for app name ADSK
            if (buffer != null)
            {
                ed.WriteMessage("Xdata with application name " +
                                            "ADSK is present");
                buffer.Dispose();
            }
            else
            {
                ed.WriteMessage("Xdata with application name " +
                                          "ADSK is not present");
            }
            tr.Commit();
        }
        catch
        {
            tr.Abort();
        }
    }
}

