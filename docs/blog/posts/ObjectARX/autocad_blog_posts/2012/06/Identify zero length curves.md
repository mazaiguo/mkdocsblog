---
title: "Identify zero length curves"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "You can use database API “EraseEmptyObjects” to identify the zero length curves. This API can be used to erase the zero length curves or API can be..."
author: Autodesk
---
# Identify zero length curves

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identify-zero-length-curves.html

## 文章内容

By Virupaksha Aithal
You can use database API “EraseEmptyObjects” to identify the zero length curves. This API can be used to erase the zero length curves or API can be used with database reactor to get the list of zero length curves as shown in below code
static ObjectIdCollection erasedIds = new ObjectIdCollection();
  [CommandMethod("ZeroLengthCurves")]
static public void ZeroLengthCurves()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      //clear
    erasedIds.Clear();
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        db.ObjectErased +=
                        new ObjectErasedEventHandler(db_ObjectErased);
        db.EraseEmptyObjects((int)(EraseFlags.ZeroLengthCurve));
        ed.WriteMessage("Zero length curves count = "
                                + erasedIds.Count.ToString() + "\n");
        db.ObjectErased -=
                        new ObjectErasedEventHandler(db_ObjectErased);
          //abort
        tr.Abort();
    }
}
  static void db_ObjectErased(object sender, ObjectErasedEventArgs e)
{
    erasedIds.Add(e.DBObject.ObjectId);
}

