---
title: "Locking the layer through .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Layer
description: "Each layer (layer table record) exposes “IsLocked” property. You can set the “IsLocked” to true to lock the layer. Below code shows the procedure t..."
author: Autodesk
---
# Locking the layer through .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/locking-the-layer-through-net.html

## 文章内容

By Virupaksha Aithal
Each layer (layer table record) exposes “IsLocked” property. You can set the “IsLocked” to true to lock the layer. Below code shows the procedure to so the same. Below code to work, there should be layer called “Test” in the document.
[CommandMethod("Layerlack")]
static public void Layerlack()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        LayerTable table = tr.GetObject(db.LayerTableId,
                                    OpenMode.ForRead) as LayerTable;
          if (table.Has("Test"))
        {
            LayerTableRecord record = tr.GetObject(table["Test"],
                              OpenMode.ForWrite) as LayerTableRecord;
            record.IsLocked = true;
            //rset the line weight Just make layer dirty..
            record.LineWeight = record.LineWeight;
        }
        tr.Commit();
    }
    ed.Regen();
}

## 评论

**内容**: petcon said...
rset the line weight Just make layer dirty..
i do not understand what this mean
Reply
06/12/2012 at 09:29 PM

---
**内容**: tiancao1001 said...
rset the line weight Just make layer dirty..
是什么意思，好像也没起什么作业？是系统变量LAYLOCKFADECTL的淡入度吗？
Reply
04/13/2021 at 02:04 AM

---
**内容**: tiancao1001 said...
应该就是 LAYLOCKFADECTL 变量 相同的意思
Reply
04/13/2021 at 02:27 AM

---
